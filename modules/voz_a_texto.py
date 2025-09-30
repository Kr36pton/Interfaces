import streamlit as st
from pathlib import Path
import whisper
import tempfile
import os

def render():
    st.title("Voz → Texto (Whisper)")

    st.markdown("Sube un archivo WAV, MP3 u otro formato compatible y obtén la transcripción usando Whisper.")

    # Subir archivo de audio
    uploaded = st.file_uploader("Subir archivo de audio", type=["wav", "mp3", "m4a", "ogg", "flac"])

    if uploaded is not None:
        # Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp_file:
            tmp_file.write(uploaded.read())
            tmp_path = tmp_file.name

        st.audio(tmp_path)  # Reproducir audio subido

        if st.button("Procesar audio"):
            with st.spinner("Transcribiendo con Whisper..."):
                try:
                    model = whisper.load_model("small")  # Puedes cambiar a "base", "medium" o "large"
                    result = model.transcribe(tmp_path)
                    text = result["text"].strip()
                except Exception as e:
                    st.error(f"Error en la transcripción: {e}")
                    text = None

            if text:
                st.success("Transcripción completada.")
                st.text_area("Texto reconocido", text, height=200)
                st.download_button("Descargar TXT", data=text, file_name="transcripcion.txt", mime="text/plain")
            else:
                st.warning("No se pudo transcribir el audio.")

        # Eliminar archivo temporal
        os.remove(tmp_path)
