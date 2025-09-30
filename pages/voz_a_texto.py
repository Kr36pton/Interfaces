import streamlit as st

def render():
    st.title("Voz → Texto (Whisper)")
    st.markdown("Página en desarrollo. Funcionalidad prevista:")
    st.markdown("""
- Subir archivo de audio o grabar desde el micrófono.
- Detectar idioma y permitir selección de idioma de salida.
- Mostrar transcripción y opción de descarga.
    """)
