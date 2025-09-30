import streamlit as st
import importlib

st.set_page_config(page_title="Suite Multimedia — Herramientas IA", layout="wide")

# Estilos mínimos para una estética limpia (rosado claro / dorado / nude)
st.markdown(
    """
    <style>
    :root{
        --bg:#fffaf8;
        --card:#fff;
        --accent:#f7d6e0;
        --muted:#bfa6a0;
        --gold:#cfa46b;
    }
    .reportview-container, .main{
        background: var(--bg);
    }
    header {background: linear-gradient(90deg, rgba(247,214,224,0.25), rgba(255, 250, 245, 0.5));}
    .css-1v0mbdj.e1fqkh3o1 {padding-top: 1rem;} /* small top padding */
    .stSidebar .css-1d391kg {width: 270px;} /* sidebar width */
    .stButton>button {border-radius: 8px;}
    .page-card {
        background: var(--card);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .muted {color: var(--muted); font-size:13px;}
    .accent-title {color: #b24d6c;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Páginas: mapeo título legible -> módulo dentro de la carpeta pages
PAGES = {
    "Inicio": "pages.inicio",
    "Texto → Audio (gTTS)": "pages.texto_a_audio",
    "Voz → Texto (Whisper)": "pages.voz_a_texto",
    "OCR (Imagen → Texto)": "pages.ocr",
    "OCR → Traducción → Audio": "pages.ocr_audio",
    "NLP: Sentimiento, TF-IDF y Palabras clave": "pages.nlp_textblob",
    "Detección de Objetos (YOLO)": "pages.deteccion_objetos",
    "Reconocimiento de Gestos (Teachable Machine)": "pages.reconocimiento_gestos",
    "Chatbot sobre PDF (LLM)": "pages.chatbot_pdf",
    "Descripción de Imágenes y QA": "pages.interpretacion_imagen",
}

with st.sidebar:
    st.title("Navegación")
    choice = st.radio("", list(PAGES.keys()), index=0)
    st.markdown("---")
    st.markdown("Estructura del proyecto: `/pages/(herramienta).py`")
    st.markdown("Mantener un diseño limpio y consistente.")

# Importar y ejecutar la página seleccionada
module_path = PAGES[choice]
try:
    page = importlib.import_module(module_path)
    if hasattr(page, "render"):
        page.render()
    else:
        st.error(f"El módulo {module_path} existe pero no define `render()`.")
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
