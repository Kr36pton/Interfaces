import streamlit as st
from PIL import Image
import pytesseract
import io

def render():
    st.title("OCR (Imagen → Texto)")
    st.markdown("Extrae texto de imágenes usando **Tesseract OCR**.")

    uploaded_file = st.file_uploader(
        "Sube una imagen (JPG, PNG, TIFF, BMP)",
        type=["jpg", "jpeg", "png", "tiff", "bmp"]
    )

    if uploaded_file:
        try:
            image = Image.open(io.BytesIO(uploaded_file.read()))
        except Exception as e:
            st.error(f"No se pudo abrir la imagen: {e}")
            return

        st.image(image, caption="Imagen cargada", use_container_width=True)

        if st.button("Procesar imagen"):
            with st.spinner("Extrayendo texto..."):
                try:
                    text = pytesseract.image_to_string(image, lang="spa+eng")
                except Exception as e:
                    st.error(f"Error al aplicar OCR: {e}")
                    return

            st.success("OCR completado")
            st.markdown("#### Texto detectado")
            st.text_area("Resultado OCR", text.strip(), height=250)

            st.download_button(
                "Descargar texto",
                data=text.strip(),
                file_name="ocr_resultado.txt",
                mime="text/plain"
            )
