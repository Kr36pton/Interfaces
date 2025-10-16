import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="🧰",
    layout="wide",
)

# Estilos: forzar esquema claro y buen contraste. Ocultar menú nativo.
st.markdown(
    """
    <style>
      /* Ocultar navegación multipágina nativa */
      section[data-testid="stSidebarNav"] { display: none !important; }

      /* Forzar fondo claro y texto oscuro en toda la app */
      html, body,
      .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stMainBlockContainer"],
      [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
        filter: none !important;
        opacity: 1 !important;
      }

      /* Tipografías y encabezados en negro */
      h1, h2, h3, h4, h5, h6,
      .stMarkdown, .stText, .stCaption, label, p, span, div {
        color: #111111 !important;
      }

      /* Inputs, botones, radios y tablas con bordes suaves en claro */
      .stButton>button,
      .stDownloadButton>button,
      .st-radio [role="radiogroup"] label,
      .stTextInput input,
      .stTextArea textarea,
      .stSelectbox [data-baseweb="select"] {
        color: #111111 !important;
        background: #ffffff !important;
        border: 1px solid #e6e6e6 !important;
        border-radius: 10px !important;
      }

      /* Sidebar visual limpio */
      [data-testid="stSidebar"] .stMarkdown h1,
      [data-testid="stSidebar"] .stMarkdown h2,
      [data-testid="stSidebar"] .stMarkdown h3 {
        color: #111111 !important;
      }

      /* Tarjeta opcional para secciones */
      .page-card {
        background: #ffffff !important;
        border: 1px solid #efefef !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
      }
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
