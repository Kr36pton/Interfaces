import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="🧰",
    layout="wide",
)

# Tema oscuro coherente
st.markdown(
    """
    <style>
      section[data-testid="stSidebarNav"] { display: none !important; }
      :root{
        --bg:#0f1115; --card:#151924; --text:#e8e8ea; --muted:#a5a8b3; --border:#222634; --accent:#5b9cff;
      }
      html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
      [data-testid="stToolbar"], [data-testid="stMainBlockContainer"], [data-testid="stSidebar"]{
        background-color: var(--bg) !important; color: var(--text) !important; filter:none !important; opacity:1 !important;
      }
      h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stCaption, label, p, span, div { color: var(--text) !important; }
      small, .stCaption { color: var(--muted) !important; }
      .page-card, .stAlert, .stDataFrame, .stTable, .stPlotlyChart, .stMetric, .stCheckbox, .stRadio {
        background-color: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 8px;
      }
      .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"],
      .stNumberInput input, .stDateInput input, .stTimeInput input {
        background-color: var(--card) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: 10px !important;
      }
      .stButton>button, .stDownloadButton>button {
        background: var(--accent) !important; color: #ffffff !important; border: 0 !important; border-radius: 10px !important;
      }
      .stButton>button:hover, .stDownloadButton>button:hover { filter: brightness(1.05); }
      [data-testid="stSidebar"] { border-right: 1px solid var(--border) !important; }
      .stRadio [role="radiogroup"] label { color: var(--text) !important; }
      .stRadio [role="radio"] { background: var(--card) !important; border: 1px solid var(--border) !important; }
      .stDataFrame thead tr th, .stDataFrame tbody tr td { color: var(--text) !important; background-color: var(--card) !important; }
      img, canvas, svg { filter: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mapeo a un solo módulo por página
PAGES = {
    "Inicio": "modules.inicio",
    "Texto → Audio (gTTS)": "modules.texto_a_audio",
    "Voz → Texto (Vosk)": "modules.voz_a_texto",
    "OCR (Imagen → Texto)": "modules.ocr",
    "OCR → Traducción → Audio": "modules.ocr_audio",
    "NLP: Sentimiento, TF-IDF y Palabras clave": "modules.nlp_textblob",
    "Identificación de objetos (YOLO)": "modules.deteccion_objetos",
    "Identificación de gestos (Teachable Machine)": "modules.reconocimiento_gestos",
}

with st.sidebar:
    st.title("Navegación")
    choice = st.radio(
        "Selecciona una página:",
        list(PAGES.keys()),
        index=0,
        label_visibility="collapsed",
    )

module_path = PAGES[choice]
try:
    page_module = importlib.import_module(module_path)
    if hasattr(page_module, "render") and callable(page_module.render):
        page_module.render()
    else:
        st.error(f"El módulo {module_path} no define render().")
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
