import streamlit as st
import io
import wave
import json
from vosk import Model, KaldiRecognizer

# Cargar modelo Vosk (pequeño en español)
@st.cache_resource
def load_model():
    return Model("models/vosk-model-small-es-0.42")

def transcribe(wav_bytes, model):
    wf = wave.open(io.BytesIO(wav_bytes), "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    text_parts = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if res.get("text"):
                text_parts.append(res["text"])
    res = json.loads(rec.FinalResult())
    if res.get("text"):
        text_parts.append(res["text"])
    return " ".join(text_parts).strip()

def render():
    st.title("Voz → Texto (Vosk offline)")
    st.markdown("Sube un archivo WAV y obtén la transcripción sin ffmpeg.")

    # Solo subir archivo WAV
    uploaded = st.file_uploader("Subir archivo WAV", type=["wav"])

    wav_bytes = None
    if uploaded is not None:
        wav_bytes = uploaded.read()
        st.audio(wav_bytes, format="audio/wav")  # Opcional: escuchar el audio subido

    if wav_bytes and st.button("Procesar audio"):
        with st.spinner("Transcribiendo..."):
            try:
                model = load_model()
                text = transcribe(wav_bytes, model)
            except Exception as e:
                st.error(f"Error en la transcripción: {e}")
                return

        if text:
            st.success("Transcripción completada.")
            st.text_area("Texto reconocido", text, height=200)
            st.download_button("Descargar TXT", data=text, file_name="transcripcion.txt", mime="text/plain")
        else:
            st.warning("No se reconoció texto en el audio.")
