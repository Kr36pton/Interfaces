import streamlit as st
import tempfile
import os
import whisper
import torch
from audiorecorder import audiorecorder

def load_model(size="base"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model(size, device=device)

def save_temp_audio(data_bytes):
    """Guardar bytes de audio en un archivo temporal wav"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(data_bytes)
        return tmp.name

def render():
    st.title("Voz → Texto (Whisper)")
    st.markdown("Sube o graba audio para transcribir o traducir con Whisper.")

    # Configuración
    col1, col2 = st.columns([1,1])
    with col1:
        mode = st.radio("Modo", ["Transcribir", "Traducir"], index=0)
    with col2:
        model_size = st.selectbox("Modelo Whisper", ["tiny", "base", "small", "medium"], index=1)

    # Idiomas destino solo si está en modo "Traducir"
    target_lang = None
    if mode == "Traducir":
        target_lang = st.selectbox(
            "Idioma destino",
            ["en", "es", "fr", "de", "it", "pt"],
            index=0,
            help="Código ISO del idioma destino"
        )

    st.markdown("### Opción 1: Subir archivo de audio")
    uploaded_file = st.file_uploader("Selecciona un archivo (mp3, wav, m4a, ogg)", type=["mp3","wav","m4a","ogg"])

    st.markdown("### Opción 2: Grabar desde el navegador")
    audio = audiorecorder("Grabar", "Detener")

    # Cuando haya archivo o grabación disponible
    audio_path = None
    if uploaded_file is not None:
        audio_path = save_temp_audio(uploaded_file.read())
    elif len(audio) > 0:
        audio_bytes = audio.tobytes()
        st.audio(audio_bytes, format="audio/wav")
        audio_path = save_temp_audio(audio_bytes)

    if audio_path and st.button("Procesar audio"):
        with st.spinner("Procesando..."):
            try:
                model = load_model(model_size)
                if mode == "Transcribir":
                    result = model.transcribe(audio_path, task="transcribe")
                else:
                    result = model.transcribe(audio_path, task="translate")
            except Exception as e:
                st.error(f"Error al transcribir: {e}")
                return
            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)

        st.success("Procesamiento completado.")
        st.markdown("#### Texto reconocido")
        st.text_area("Salida", result.get("text","").strip(), height=200)

        st.markdown("#### Idioma detectado")
        st.write(f"**{result.get('language','?')}**")

        st.download_button(
            "Descargar transcripción",
            data=result.get("text","").strip(),
            file_name="transcripcion.txt",
            mime="text/plain"
        )
