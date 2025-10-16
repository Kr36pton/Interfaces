import streamlit as st
from PIL import Image
import numpy as np
import io
import time
import re

# NLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Intentar modelo de captioning (Transformers)
_CAPTION_OK = False
try:
    import torch
    from transformers import pipeline
    _CAPTION_OK = True
except Exception:
    _CAPTION_OK = False

# Fallbacks: detección y OCR
_YOLO_OK = False
try:
    from ultralytics import YOLO
    _YOLO_OK = True
except Exception:
    _YOLO_OK = False

_OCR_OK = False
try:
    import easyocr
    _OCR_OK = True
except Exception:
    _OCR_OK = False


# ---------------------------
# Utilidades
# ---------------------------
def _sentencize(text: str):
    if not text:
        return []
    raw = re.split(r"(?<=[\.\?\!])\s+|\n{1,}", text)
    sents = [re.sub(r"\s+", " ", s).strip() for s in raw if s and re.sub(r"\s+", " ", s).strip()]
    return sents

@st.cache_resource(show_spinner=False)
def _load_caption_pipeline(model_name: str = "Salesforce/blip-image-captioning-base"):
    device = 0 if torch.cuda.is_available() else -1
    return pipeline("image-to-text", model=model_name, device=device)

@st.cache_resource(show_spinner=False)
def _load_yolo(model_name: str = "yolov8n.pt"):
    model = YOLO(model_name)
    if torch.cuda.is_available():
        model.to("cuda")
    return model

@st.cache_resource(show_spinner=False)
def _load_ocr():
    # Idiomas comunes: español+inglés
    return easyocr.Reader(["es", "en"], gpu=torch.cuda.is_available() if torch.cuda.is_available() else False)

def _caption_transformers(pil_img: Image.Image, model_choice: str):
    cap_pipe = _load_caption_pipeline(model_choice)
    t0 = time.time()
    out = cap_pipe(pil_img, max_new_tokens=30)
    latency = time.time() - t0
    text = (out[0]["generated_text"] if isinstance(out, list) and out else "").strip()
    return text, latency

def _describe_heuristic(pil_img: Image.Image, conf_th: float = 0.3):
    parts = []
    latency = 0.0

    # YOLO
    if _YOLO_OK:
        model = _load_yolo()
        t0 = time.time()
        res = model.predict(np.array(pil_img), conf=conf_th, verbose=False)
        latency += time.time() - t0
        names = res[0].names if res and len(res) else {}
        det = res[0].boxes if res and len(res) else None
        if det is not None and len(det) > 0:
            cls = det.cls.detach().cpu().numpy().astype(int)
            conf = det.conf.detach().cpu().numpy()
            items = [names.get(int(c), str(int(c))) for c in cls]
            # Resumen de objetos
            if items:
                uniq = {}
                for it in items:
                    uniq[it] = uniq.get(it, 0) + 1
                obj_str = ", ".join([f"{k}×{v}" if v > 1 else k for k, v in sorted(uniq.items(), key=lambda x: (-x[1], x[0]))])
                parts.append(f"Objetos detectados: {obj_str}.")
    else:
        parts.append("Detección de objetos no disponible.")

    # OCR
    if _OCR_OK:
        reader = _load_ocr()
        t0 = time.time()
        txts = reader.readtext(np.array(pil_img), detail=0)
        latency += time.time() - t0
        txts = [t.strip() for t in txts if isinstance(t, str) and t.strip()]
        if txts:
            ocr_text = " ".join(txts)
            parts.append(f"Texto en la imagen: “{ocr_text}”.")
    else:
        parts.append("OCR no disponible.")

    desc = " ".join(parts).strip()
    return desc, latency

def _build_knowledge(description: str, extra_notes: str = ""):
    base = description.strip()
    notes = extra_notes.strip()
    all_text = base if not notes else f"{base}\n{notes}"
    sents = _sentencize(all_text)
    # Garantizar que haya algo indexable
    if not sents and all_text:
        sents = [all_text]
    return sents

def _qa_over_description(sentences, question, top_k=3, threshold=0.25):
    if not sentences:
        return []
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences + [question])
    q_vec = X[-1]
    D = X[:-1]
    sims = cosine_similarity(q_vec, D).ravel()
    order = np.argsort(sims)[::-1][:top_k]
    hits = [(int(i), float(sims[i]), sentences[i]) for i in order if float(sims[i]) >= threshold]
    return hits


# ---------------------------
# Página
# ---------------------------
def render():
    st.title("Interpretación de imágenes — Descripción y Q&A")
    st.markdown(
        "Sube una imagen. Se genera una **descripción detallada** con un modelo de captioning o heurísticas "
        "(detección de objetos + OCR). Luego puedes **hacer preguntas** sobre la imagen."
    )

    with st.expander("Opciones de modelo", expanded=False):
        colm = st.columns(3)
        with colm[0]:
            mode = st.selectbox(
                "Método de descripción",
                ["Transformers: BLIP (image-to-text)", "Heurístico: YOLO + OCR"],
                index=0 if _CAPTION_OK else 1,
                help="BLIP ofrece mejor lenguaje pero requiere descargar pesos. Heurístico combina detección y OCR."
            )
        with colm[1]:
            cap_model = st.selectbox(
                "Modelo de captioning",
                ["Salesforce/blip-image-captioning-base", "Salesforce/blip-image-captioning-large"],
                index=0,
                disabled=(mode != "Transformers: BLIP (image-to-text)" or not _CAPTION_OK),
                help="Modelos aprox. ~990MB (large) / ~400MB (base)."
            )
        with colm[2]:
            conf_th = st.slider("Confianza YOLO (heurístico)", 0.10, 0.90, 0.30, 0.05, disabled=(mode != "Heurístico: YOLO + OCR"))

    uploaded = st.file_uploader("Sube una imagen (JPG/PNG/WebP)", type=["jpg", "jpeg", "png", "webp"])
    if not uploaded:
        return

    pil_img = Image.open(io.BytesIO(uploaded.read())).convert("RGB")
    st.image(pil_img, caption="Imagen cargada", use_container_width=True)

    if st.button("Generar descripción"):
        with st.spinner("Analizando imagen..."):
            if mode.startswith("Transformers") and _CAPTION_OK:
                try:
                    desc, latency = _caption_transformers(pil_img, cap_model)
                    meta = f"Captioning (BLIP). Latencia: {latency:.2f}s."
                except Exception as e:
                    st.warning(f"Fallo en captioning: {e}. Usando heurístico.")
                    desc, latency = _describe_heuristic(pil_img, conf_th=conf_th)
                    meta = f"Heurístico (YOLO+OCR). Latencia: {latency:.2f}s."
            else:
                desc, latency = _describe_heuristic(pil_img, conf_th=conf_th)
                meta = f"Heurístico (YOLO+OCR). Latencia: {latency:.2f}s."

        if not desc.strip():
            st.error("No se pudo generar una descripción útil.")
            return

        st.success("Descripción generada.")
        st.markdown("**Descripción**")
        st.write(desc)
        st.caption(meta)

        # Construir base de conocimiento para Q&A
        sentences = _build_knowledge(desc)
        st.session_state["img_desc_sentences"] = sentences

    if "img_desc_sentences" not in st.session_state:
        return

    st.markdown("---")
    st.subheader("Preguntas sobre la imagen")
    q = st.text_input("Pregunta")
    topk = st.slider("Fragmentos a mostrar", 1, 5, 3)
    thr = st.slider("Umbral de similitud", 0.0, 1.0, 0.25, 0.01)

    if q:
        with st.spinner("Buscando en la descripción..."):
            hits = _qa_over_description(st.session_state["img_desc_sentences"], q, top_k=topk, threshold=thr)

        if not hits:
            st.warning("No hay fragmentos suficientemente relevantes. Reformula la pregunta o baja el umbral.")
            return

        for idx, score, frag in hits:
            st.markdown(f"**Fragmento {idx} — similitud: {score:.3f}**")
            st.write(frag)
            st.markdown("---")


# Punto de entrada para Streamlit multipágina
if __name__ == "__main__":
    render()
