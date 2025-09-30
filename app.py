import streamlit as st
import importlib

st.set_page_config(page_title="Suite Multimedia — Herramientas IA", layout="wide")

# Ocultar el menú de páginas automático de Streamlit y estilos generales
st.markdown(
    """
    <style>
    /* Ocultar el menú de páginas automático de Streamlit */
    section[data-testid="stSidebarNav"] {display: none;}
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
    .css-1v0mbdj.e1fqkh3o1 {padding-top: 1rem;}
    .stSidebar .css-1d391kg {width: 270px;}
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

# Mapeo de páginas -> módulos dentro de la carpeta `modules`
PAGES = {
    "Inicio": "modules.inicio",
    "Texto → Audio (gTTS)": "modules.texto_a_audio",
    "Voz → Texto (Whisper)": "modules.voz_a_texto",
    "OCR (Imagen → Texto)": "modules.ocr",
    "OCR → Traducción → Audio": "modules.ocr_audio",
    "NLP: Sentimiento, TF-IDF y Palabras clave": "modules.nlp_textblob",
    "Detección de Objetos (YOLO)": "modules.deteccion_objetos",
    "Reconocimiento de Gestos (Teachable Machine)": "modules.reconocimiento_gestos",
    "Chatbot sobre PDF (LLM)": "modules.chatbot_pdf",
    "Descripción de Imágenes y QA": "modules.interpretacion_imagen",
}

with st.sidebar:
    st.title("Navegación")
    choice = st.radio("", list(PAGES.keys()), index=0)
    st.markdown("---")
    st.markdown("Estructura del proyecto: `/modules/(herramienta).py`")

module_path = PAGES[choice]
try:
    page = importlib.import_module(module_path)
    if hasattr(page, "render"):
        page.render()
    else:
        st.error(f"El módulo {module_path} existe pero no define `render()`.")
except ModuleNotFoundError:
    st.error(
        f"Error: no se encontró el módulo '{module_path}'. Asegúrate de que exista el archivo `{module_path.replace('.', '/')}.py` y de tener `modules/__init__.py`."
    )
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
