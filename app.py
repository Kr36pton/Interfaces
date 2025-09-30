# app.py
import streamlit as st
import importlib


st.set_page_config(page_title="Herramientas Multimodales", layout="wide")


PAGES = [
("Inicio", "Interfaces.pages.home"),
("Texto → Audio", "Interfaces.pages.texto_a_audio"),
("Voz → Texto", "Interfaces.pages.voice_to_text"),
("OCR (Imagen → Texto)", "Interfaces.pages.ocr"),
("OCR + Traducción + Audio", "Interfaces.pages.ocr_text_to_audio"),
("NLP: TextBlob / NLTK", "Interfaces.pages.nlp_textblob"),
("Detección de Objetos (YOLO)", "Interfaces.pages.ident_objetos_yolo"),
("Identificación de Gestos", "Interfaces.pages.ident_gestos"),
("Chatbot con PDF (LLM)", "Interfaces.pages.nlp_chatbot"),
("Interpretación de Imágenes", "Interfaces.pages.interpre_imagen"),
]


st.sidebar.title("Navegación")
selection = st.sidebar.radio("Ir a", [p[0] for p in PAGES], index=0)


module_path = next(p[1] for p in PAGES if p[0] == selection)


try:
module = importlib.import_module(module_path)
if hasattr(module, "app"):
module.app()
else:
st.error(f"El módulo {module_path} no define la función 'app()'.")
except Exception as e:
st.error(f"Error cargando la página '{selection}': {e}")
