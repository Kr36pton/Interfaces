import streamlit as st
import io
import re
from typing import List, Tuple

import numpy as np
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Opcional: embeddings si está disponible (fallback automático a TF-IDF)
_EMB_OK = False
try:
    from sentence_transformers import SentenceTransformer
    _EMB_OK = True
except Exception:
    _EMB_OK = False


# ---------------------------
# Utilidades de extracción
# ---------------------------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        texts.append(txt)
    return "\n".join(texts)


# ---------------------------
# Chunking
# ---------------------------
def normalize_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).replace("\r", "").strip()

def split_into_sentences(text: str) -> List[str]:
    # Split robusto sin NLTK: puntos, signos, saltos de línea
    # Conserva el separador como fin de oración.
    raw = re.split(r"(?<=[\.\?\!])\s+|\n{2,}", text)
    sentences = [normalize_whitespace(s) for s in raw if s and normalize_whitespace(s)]
    return sentences

def make_chunks(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """
    Construye chunks aproximados por longitud de caracteres, respetando oraciones cuando sea posible.
    chunk_size y overlap en número de caracteres para controlar densidad semántica.
    """
    sentences = split_into_sentences(text)
    chunks = []
    buf = ""
    for s in sentences:
        if len(buf) + len(s) + 1 <= chunk_size:
            buf = f"{buf} {s}".strip()
        else:
            if buf:
                chunks.append(buf)
            # inicio del siguiente chunk con solapamiento
            if overlap > 0 and chunks:
                tail = chunks[-1][-overlap:]
                buf = f"{tail} {s}".strip()
            else:
                buf = s
    if buf:
        chunks.append(buf)
    # Fallback si no hubo oraciones
    if not chunks and text:
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i : i + chunk_size])
    return chunks


# ---------------------------
# Indexadores
# ---------------------------
class TFIDFIndexer:
    def __init__(self, stoplist: List[str] = None):
        self.stoplist = stoplist
        self.vectorizer = TfidfVectorizer(
            stop_words=self.stoplist, max_df=0.9, min_df=1, ngram_range=(1, 2)
        )
        self._X = None
        self._chunks = None

    def fit(self, chunks: List[str]):
        self._chunks = chunks
        self._X = self.vectorizer.fit_transform(chunks)

    def query(self, q: str, top_k: int = 3) -> List[Tuple[int, float]]:
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self._X).ravel()
        order = np.argsort(sims)[::-1][:top_k]
        return [(int(i), float(sims[i])) for i in order]


class EmbeddingIndexer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if not _EMB_OK:
            raise RuntimeError("sentence-transformers no disponible")
        self.model = SentenceTransformer(model_name)
        self._E = None
        self._chunks = None

    def fit(self, chunks: List[str]):
        self._chunks = chunks
        self._E = self.model.encode(chunks, normalize_embeddings=True, show_progress_bar=False)

    def query(self, q: str, top_k: int = 3) -> List[Tuple[int, float]]:
        q_emb = self.model.encode([q], normalize_embeddings=True, show_progress_bar=False)[0]
        sims = (self._E @ q_emb)
        order = np.argsort(sims)[::-1][:top_k]
        return [(int(i), float(sims[i])) for i in order]


# ---------------------------
# Página
# ---------------------------
def render():
    st.title("Chatbot sobre PDF (NLP / LLM)")
    st.markdown(
        "Sube un PDF, se extrae el texto, se indexa en *chunks* y se recupera el fragmento más relevante para tu pregunta. "
        "Modo básico: TF-IDF + coseno. Modo avanzado opcional: embeddings."
    )

    with st.expander("Parámetros de indexación", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            chunk_size = st.slider("Tamaño de chunk (caracteres)", 600, 2400, 1200, 100)
        with col_b:
            overlap = st.slider("Solapamiento (caracteres)", 0, 600, 200, 50)
        with col_c:
            use_embeddings = st.checkbox("Usar embeddings (sentence-transformers)", value=False, disabled=not _EMB_OK)
        if not _EMB_OK and use_embeddings:
            st.warning("sentence-transformers no está disponible; usando TF-IDF.")

    uploaded = st.file_uploader("Sube un PDF", type=["pdf"])

    if not uploaded:
        return

    if st.button("Procesar PDF"):
        with st.spinner("Extrayendo texto..."):
            raw_text = extract_text_from_pdf(uploaded.read())

        if not raw_text or not raw_text.strip():
            st.error("No se pudo extraer texto utilizable del PDF.")
            return

        with st.spinner("Construyendo chunks..."):
            chunks = make_chunks(raw_text, chunk_size=chunk_size, overlap=overlap)

        st.success(f"Procesado. Chunks: {len(chunks)}")
        st.session_state["pdf_chunks"] = chunks
        st.session_state["pdf_ready"] = True

    if not st.session_state.get("pdf_ready"):
        return

    chunks = st.session_state["pdf_chunks"]

    # Construir índice bajo demanda o si se cambia el modo
    if use_embeddings and _EMB_OK:
        if "emb_index" not in st.session_state or st.session_state.get("emb_index_params") != (len(chunks), chunk_size, overlap):
            with st.spinner("Indexando (embeddings)..."):
                emb_index = EmbeddingIndexer()
                emb_index.fit(chunks)
                st.session_state["emb_index"] = emb_index
                st.session_state["emb_index_params"] = (len(chunks), chunk_size, overlap)
        indexer = st.session_state["emb_index"]
        score_label = "sim_emb"
    else:
        # Stoplist simple ES+EN sin NLTK para evitar descargas
        stoplist = [
            "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una",
            "su","al","lo","como","más","pero","sus","le","ya","o","este","sí","porque","esta","entre",
            "cuando","muy","sin","sobre","también","me","hasta","hay","donde","quien","desde","todo",
            "nos","durante","todos","uno","les","ni","contra","otros","ese","eso","ante","ellos","e",
            "esto","mí","antes","algunos","qué","unos","yo","otro","otras","otra","él","tanto","esa","estos",
            "mucho","quienes","nada","muchos","cual","poco","ella","estar","estas","algunas","algo","nosotros",
            "mi","mis","tú","te","ti","tu","tus","ellas","nosotras","vosotros","vosotras","os","mío","mía",
            "míos","mías","tuyo","tuya","tuyos","tuyas","suyo","suya","suyos","suyas","nuestro","nuestra",
            "nuestros","nuestras","vuestro","vuestra","vuestros","vuestras","esos","esas","estoy","estás",
            "está","estamos","estáis","están","esté","estés","estemos","estéis","estén","estaré","estarás",
            "estará","estaremos","estaréis","estarán","he","has","ha","hemos","habéis","han","haya","hayas",
            "ing","the","and","to","of","in","that","is","for","on","it","with","as","are","was","at","by",
            "be","this","from","or","an","which","but","not","have","has","had","were","their","they","you",
            "we","his","her","its","can","all","one","more","about","there","been","if","when","who","will",
            "would","what","so","no","up","out","do","into","than","your","them","could","my","over","some"
        ]
        if "tfidf_index" not in st.session_state or st.session_state.get("tfidf_index_params") != (len(chunks), chunk_size, overlap):
            with st.spinner("Indexando (TF-IDF)..."):
                tfidf_index = TFIDFIndexer(stoplist=stoplist)
                tfidf_index.fit(chunks)
                st.session_state["tfidf_index"] = tfidf_index
                st.session_state["tfidf_index_params"] = (len(chunks), chunk_size, overlap)
        indexer = st.session_state["tfidf_index"]
        score_label = "sim_tfidf"

    st.markdown("---")
    q = st.text_input("Pregunta")
    topk = st.slider("Resultados a mostrar", 1, 5, 3, 1)
    threshold = st.slider("Umbral de similitud", 0.0, 1.0, 0.25, 0.01)

    if q:
        with st.spinner("Buscando fragmentos relevantes..."):
            hits = indexer.query(q, top_k=topk)

        shown = False
        for i, score in hits:
            if score < threshold:
                continue
            frag = chunks[i]
            st.markdown(f"**Fragmento {i} — {score_label}: {score:.3f}**")
            st.write(frag)
            st.markdown("---")
            shown = True

        if not shown:
            st.warning("No hay fragmentos suficientemente relevantes. Reformula la pregunta o ajusta el umbral.")
