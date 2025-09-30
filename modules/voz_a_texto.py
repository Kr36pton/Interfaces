import streamlit as st
import tempfile
import os
import whisper
import torch
from pydub import AudioSegment

def load_model():
    # Cargar Whisper en el dispositivo disponible
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model("base", device=device)

@st.cache_resource
def get_model():
    return load_model()

def convert_to_wav(uploaded_file):
    # Guardar archivo temporal y convertir a WAV con pydub
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        tmp_in.write(uploaded_file.read())
        tmp_in.flush()
        tmp_in_path = tmp_in.name

    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_out_path = tmp_out.name
    tmp_out.close()

    audio = AudioSegment.from_file(tmp_in_path)
    audio.export(tmp_out_path, format="wav")

    return tmp_out_path

def render():
    st.title("Voz → Texto (Whisper)")
    st.markdown("Transcribe audio a texto usando **OpenAI Whisper**.")

    st.markdown("#### Subir archivo de audio")
    uploaded_file = st.file_uploader("Selecciona un archivo de audio (mp3, wav, m4a, ogg...)", type=["mp3", "wav", "m4a", "ogg"])

    st.markdown("#### Opciones")
    col1, col2 = st.columns([1,1])
    with col1:
        task = st.radio("Modo", ["transcribe", "translate"], index=0, help="Transcribe = en idioma original. Translate = traduce al inglés.")
    with col2:
        model_size = st.selectbox("Modelo Whisper", ["base", "small", "medium"], index=0)

    if st.button("Procesar audio"):
        if uploaded_file is None:
            st.error("Debes subir un archivo de audio.")
            return

        with st.spinner("Procesando..."):
            # Convertir audio a wav temporal
            wav_path = convert_to_wav(uploaded_file)

            # Cargar modelo
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = whisper.load_model(model_size, device=device)

            # Transcribir
            try:
                result = model.transcribe(wav_path, task=task)
            except Exception as e:
                st.error(f"Error al transcribir: {e}")
                return

            # Mostrar resultados
            st.success("Transcripción completada.")
            st.markdown("#### Texto reconocido")
            st.text_area("Salida", result.get("text","").strip(), height=200)

            st.markdown("#### Idioma detectado")
            detected_lang = result.get("language","?")
            st.write(f"**{detected_lang}**")

            # Descargar texto
            st.download_button(
                "Descargar transcripción",
                data=result.get("text","").strip(),
                file_name="transcripcion.txt",
                mime="text/plain"
            )

            # Limpiar temporales
            os.remove(wav_path)
