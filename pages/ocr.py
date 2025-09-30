import streamlit as st

def render():
    st.title("OCR (Imagen → Texto)")
    st.markdown("Página en desarrollo. Funcionalidad prevista:")
    st.markdown("""
- Subir imagen o PDF.
- Extraer texto con Tesseract / EasyOCR.
- Mostrar texto extraído y opción de descargar como .txt.
    """)
