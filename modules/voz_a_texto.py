import streamlit as st
import whisper
import torch
import numpy as np
import soundfile as sf
import tempfile
import os
from audiorecorder import audiorecorder

def load_model(size="base"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model(size, device=device), device

def decode_wav(file_bytes):
    """Leer WAV -> numpy float32"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        data, samplerate = sf.read(tmp.name, always_2d=False)
        os.remove(tmp.name)
    if data.ndim > 1:  # estéreo a mono
        data = np.mean(data, axis=1)
    return data.astype(np.float32), samplerate

def run_inference(model, device, audio_np, sr, task="transcribe"):
    if sr != 16000:
        import librosa
        audio_np = librosa.resample(audio_np, orig_sr=sr, target_sr=16000)
        sr = 16000

    audio = whisper.pad_or_trim(audio_np)
    mel = whisper.log_mel_spectrogram(audio).to(device)

    _, probs = model.detect_language(mel)
    lang_detected = max(probs, key=probs.get)

    options = whisper.DecodingOptions(task=task)
    result = whisper.decode(model, mel, options)
    return result.text, lang_detected

def render():
    st.title("Voz → Texto (Whisper sin ffmpeg)")
    st.markdown("Solo se aceptan archivos **WAV** para garantizar compatibilidad sin ffmpeg/ffprobe.")

    col1, col2 = st.columns([1,1])
    with col1:
        mode = st.radio("Modo", ["Transcribir", "Traducir"], index=0)
    with col2:
        model_size = st.selectbox("Modelo Whisper", ["tiny", "base", "small"], index=1)

    if mode == "Traducir":
        st.info("Whisper solo traduce al inglés en este modo.")

    uploaded_file = st.file_uploader("Subir archivo de audio (solo WAV)", type=["wav"])

    st.markdown("### O grabar desde el navegador")
    audio = audiorecorder("Grabar", "Detener")

    audio_bytes = None
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
    elif len(audio) > 0:
        audio_bytes = audio.tobytes()
        st.audio(audio_bytes, format="audio/wav")

    if audio_bytes and st.button("Procesar audio"):
        with st.spinner("Procesando..."):
            try:
                model, device = load_model(model_size)
                audio_np, sr = decode_wav(audio_bytes)
                text, lang = run_inference(
                    model, device, audio_np, sr,
                    task="translate" if mode=="Traducir" else "transcribe"
                )
            except Exception as e:
                st.error(f"Error: {e}")
                return

        st.success("Completado")
        st.markdown("#### Texto reconocido")
        st.text_area("Salida", text.strip(), height=200)

        st.markdown("#### Idioma detectado")
        st.write(f"**{lang}**")

        st.download_button(
            "Descargar transcripción",
            data=text.strip(),
            file_name="transcripcion.txt",
            mime="text/plain"
        )
