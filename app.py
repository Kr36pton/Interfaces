import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="🧰",
    layout="wide",
)

st.markdown(
    """
    <style>
      /* Oculta navegación multipágina nativa */
      section[data-testid="stSidebarNav"] { display: none !important; }

      /* Colores base */
      :root{
        --bg:#0f1115;           /* fondo principal */
        --card:#151924;         /* tarjetas / paneles */
        --text:#e8e8ea;         /* texto principal */
        --muted:#a5a8b3;        /* texto secundario */
        --border:#222634;       /* bordes suaves */
        --accent:#5b9cff;       /* acento */
      }

      /* Fondo y texto global */
      html, body, .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stMainBlockContainer"],
      [data-testid="stSidebar"]{
        background-color: var(--bg) !important;
        color: var(--text) !important;
        filter:none !important;
        opacity:1 !important;
      }

      /* Tipografía y elementos de texto */
      h1, h2, h3, h4, h5, h6,
      .stMarkdown, .stText, .stCaption, label, p, span, div {
        color: var(--text) !important;
      }
      small, .markdown-text-container p em, .stCaption, .st-emotion-cache-9ycgxx {
        color: var(--muted) !important;
      }

      /* Contenedores tipo tarjeta */
      .page-card, .stAlert, .stDataFrame, .stTable, .stPlotlyChart, .stMetric, .stCheckbox, .stRadio {
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 8px;
      }

      /* Inputs y selects */
      .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"],
      .stNumberInput input, .stDateInput input, .stTimeInput input {
        background-color: var(--card) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
      }

      /* Botones */
      .stButton>button, .stDownloadButton>button {
        background: var(--accent) !important;
        color: #ffffff !important;
        border: 0 !important;
        border-radius: 10px !important;
      }
      .stButton>button:hover, .stDownloadButton>button:hover {
        filter: brightness(1.05);
      }

      /* Sidebar */
      [data-testid="stSidebar"] .stMarkdown h1,
      [data-testid="stSidebar"] .stMarkdown h2,
      [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text) !important;
      }
      [data-testid="stSidebar"] {
        border-right: 1px solid var(--border) !important;
      }

      /* Radio: bullets y etiquetas visibles en claro */
      .stRadio [role="radiogroup"] label {
        color: var(--text) !important;
      }
      .stRadio [role="radio"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
      }

      /* Tablas/Dataframes (cabeceras y celdas) */
      .stDataFrame thead tr th, .stDataFrame tbody tr td {
        color: var(--text) !important;
        background-color: var(--card) !important;
      }

      /* Imágenes y gráficos: sin filtros */
      img, canvas, svg { filter: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Páginas: permitir dos ubicaciones (modules/* o src/pages/*)
PAGES = {
    "Inicio": ["modules.inicio", "src.pages.inicio"],
    "Texto → Audio (gTTS)": ["modules.texto_a_audio", "src.pages.texto_a_audio"],
    "Voz → Texto (Vosk)": ["modules.voz_a_texto", "src.pages.voz_a_texto"],
    "OCR (Imagen → Texto)": ["modules.ocr", "src.pages.ocr"],
    "NLP: Sentimiento, TF-IDF y Palabras clave": ["modules.nlp_textblob", "src.pages.nlp_textblob"],
    "Identificación de objetos (YOLO)": ["modules.yolo_objetos", "src.pages.yolo_objetos"],
    "Identificación de gestos (Teachable Machine)": ["modules.gestos", "src.pages.gestos"],
}

def import_first(candidates):
    last_err = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError as e:
            last_err = e
            continue
    raise last_err or ModuleNotFoundError(f"No se pudo importar ninguno de: {candidates}")

with st.sidebar:
    st.title("Navegación")
    choice = st.radio(
        "Selecciona una página:",
        list(PAGES.keys()),
        index=0,
        label_visibility="collapsed",
    )

module_candidates = PAGES[choice]
try:
    page_module = import_first(module_candidates)
    if hasattr(page_module, "render") and callable(page_module.render):
        page_module.render()
    else:
        st.error(f"El módulo seleccionado no define render(). Revisar: {module_candidates}")
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
