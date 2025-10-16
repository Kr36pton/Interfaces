import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="🧰",
    layout="wide",
)

# Estilos: restaurar colores y contraste; eliminar fondos personalizados previos
st.markdown(
    """
    <style>
      /* Ocultar navegación multipágina nativa */
      section[data-testid="stSidebarNav"] { display: none; }

      /* Reset de fondos para evitar sobreexposición / bajo contraste */
      html, body,
      [data-testid="stAppViewContainer"],
      .stApp, .main,
      [data-testid="stHeader"] {
        background: unset !important;
        filter: none !important;
        opacity: 1 !important;
      }

      /* Sidebar limpio sin alterar el tema */
      [data-testid="stSidebar"] {
        background: unset !important;
      }

      /* Tarjetas opcionales */
      .page-card {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
      }

      /* Botones */
      .stButton>button { border-radius: 10px; }

      /* Radio label accesible manteniendo UI limpia */
      .sidebar-radio-label { font-weight: 600; margin-bottom: .25rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Rutas de páginas: tolera estructura modules/* o src/pages/*
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
