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
        self
