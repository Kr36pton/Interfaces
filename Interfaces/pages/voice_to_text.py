import streamlit as st




def app():
st.header("Voz → Texto (Whisper)")
st.markdown("Suba un archivo de audio (wav, mp3). La transcripción se realizará con Whisper.")


st.file_uploader("Archivo de audio", type=["wav", "mp3", "m4a"], key="whisper_audio")
st.markdown("Esta página está en estado inicial. Implementación completa tras requerimiento.")
