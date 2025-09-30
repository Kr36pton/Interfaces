import streamlit as st

def render():
    st.title("Texto → Audio (gTTS)")
    st.markdown("Página en desarrollo. Funcionalidad prevista:")
    st.markdown("""
- Entrada: caja de texto.
- Salida: reproducción en el navegador y botón de descarga (MP3).
- Parámetros: velocidad (slow/normal), idioma.
    """)
