import streamlit as st




def app():
st.header("OCR (Imagen → Texto)")
st.markdown("Carge una imagen o PDF; se extraerá el texto con pytesseract.")
st.file_uploader("Imagen o PDF", type=["png", "jpg", "jpeg", "pdf"], key="ocr_input")
st.markdown("Esta página está en estado inicial. Implementación completa tras requerimiento.")
