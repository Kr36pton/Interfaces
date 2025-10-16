import streamlit as st
import io
import os
import zipfile
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image

# TensorFlow / Keras
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_OK = True
except Exception as e:
    TF_OK = False
    TF_ERR = str(e)

# Webcam en tiempo real (opcional)
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoTransformerBase  # noqa
    WEBRTC_OK = True
except Exception:
    WEBRTC_OK = False

# ----------------------------
# Utilidades de carga de modelo
# ----------------------------
def _write_bytes_to_tempfile(data: bytes, suffix: str) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    f.write(data)
    f.flush()
    f.close()
    return f.name

def _extract_zip_to_temp(zippath: str) -> Path:
    out_dir = Path(tempfile.mkdtemp(prefix="tm_model_"))
    with zipfile.ZipFile(zippath, "r") as zf:
        zf.extractall(out_dir)
    return out_dir

def _find_labels_file(root: Path):
    for p in root.rglob("labels.txt"):
        return p
    return None

def _find_keras_model_file(root: Path):
    for name in ["keras_model.h5", "keras_model.keras"]:
        p = root / name
        if p.exists():
            return p
    for p in root.rglob("saved_model.pb"):
        return p.parent
    return None

def _read_labels_from_file(path: Path):
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    labels = [ln.split(" ", 1)[1] if " " in ln and ln.split(" ", 1)[0].isdigit() else ln for ln in lines]
    return labels

@st.cache_resource(show_spinner=False)
def load_teachable_model(model_bytes: bytes = None, labels_bytes: bytes = None):
    if not TF_OK:
        raise RuntimeError(f"TensorFlow/Keras no disponible: {TF_ERR}")
    if model_bytes is None:
        raise ValueError("Falta archivo de modelo (ZIP/.h5/.keras).")

    is_zip = model_bytes[:4] == b'PK\x03\x04'
    labels = None
    model = None

    if is_zip:
        zippath = _write_bytes_to_tempfile(model_bytes, suffix=".zip")
        root = _extract_zip_to_temp(zippath)
        labels_path = _find_labels_file(root)
        if labels_path is not None:
            labels = _read_labels_from_file(labels_path)
        model_path_candidate = _find_keras_model_file(root)
        if model_path_candidate is None:
            raise ValueError("No se encontró un modelo Keras válido dentro del ZIP.")
        if model_path_candidate.is_dir():
            model = tf.keras.models.load_model(str(model_path_candidate))
        else:
            model = load_model(str(model_path_candidate))
    else:
        # .h5 / .keras directo
        tmp = _write_bytes_to_tempfile(model_bytes, suffix=".h5")
        try:
            model = load_model(tmp)
        except Exception:
            tmp2 = _write_bytes_to_tempfile(model_bytes, suffix=".keras")
            model = load_model(tmp2)
        if labels_bytes is not None:
            labels_path = Path(_write_bytes_to_tempfile(labels_bytes, suffix=".txt"))
            labels = _read_labels_from_file(labels_path)

    if labels is None:
        raise ValueError("No se encontró labels.txt. Súbelo o inclúyelo en el ZIP.")

    input_shape = model.input_shape
    if isinstance(input_shape, list):
        input_shape = input_shape[0]
    if len(input_shape) != 4 or input_shape[-1] not in (1, 3):
        raise ValueError(f"Entrada no soportada: {input_shape}")

    _, h, w, c = input_shape
    if model.output_shape[-1] != len(labels):
        raise ValueError(f"Clases del modelo ({model.output_shape[-1]}) ≠ etiquetas ({len(labels)}).")

    return model, labels, (h, w, c)

# ----------------------------
# Predicción
# ----------------------------
def preprocess_image(img: Image.Image, target_hw_c):
    h, w, c = target_hw_c
    img = img.convert("RGB")
    img = img.resize((w, h), Image.BILINEAR)
    x = np.asarray(img).astype("float32") / 255.0
    if c == 1:
        x = np.mean(x, axis=2, keepdims=True)
    x = np.expand_dims(x, axis=0)
    return x

def predict_image(model, labels, x, top_k=5):
    preds = model.predict(x, verbose=0)[0]
    order = np.argsort(preds)[::-1][: min(top_k, len(labels))]
    return [(labels[i], float(preds[i])) for i in order]

# ----------------------------
# Webcam tiempo real (definir clase solo si WEBRTC_OK)
# ----------------------------
if WEBRTC_OK:
    from streamlit_webrtc import VideoTransformerBase  # garantía en ámbitos limitados

    class _TMVideoTransformer(VideoTransformerBase):
        def __init__(self, model_ref, labels_ref, input_hw_c, conf_th):
            super().__init__()
            self.model_ref = model_ref
            self.labels_ref = labels_ref
            self.input_hw_c = input_hw_c
            self.conf_th = conf_th

        def transform(self, frame):
            img = frame.to_image()
            x = preprocess_image(img, self.input_hw_c)
            rows = predict_image(self.model_ref, self.labels_ref, x, top_k=1)
            label, prob = rows[0]
            draw = Image.fromarray(np.array(img))
            import PIL.ImageDraw as ImageDraw
            d = ImageDraw.Draw(draw)
            txt = f"{label}: {prob:.2f}"
            d.rectangle([6, 6, 6 + 8 * len(txt) + 16, 40], fill=(0, 0, 0, 127))
            d.text((12, 12), txt, fill=(255, 255, 255))
            return draw

# ----------------------------
# Render
# ----------------------------
def render():
    st.title("Identificación de gestos (Teachable Machine)")
    if not TF_OK:
        st.error(f"No se pudo importar TensorFlow/Keras: {TF_ERR}")
        return

    st.subheader("Cargar modelo")
    c1, c2 = st.columns(2)
    with c1:
        model_file = st.file_uploader("Modelo (.zip /.h5 /.keras)", type=["zip", "h5", "keras"])
    with c2:
        labels_file = st.file_uploader("labels.txt (si no viene en el ZIP)", type=["txt"])

    if model_file is None:
        st.info("Sube el modelo para habilitar la predicción.")
        return

    try:
        model, labels, input_hw_c = load_teachable_model(
            model_bytes=model_file.read(),
            labels_bytes=(labels_file.read() if labels_file is not None else None),
        )
        st.success(f"Modelo cargado. Clases: {len(labels)}. Input: {input_hw_c}.")
    except Exception as e:
        st.error(f"Error al cargar modelo: {e}")
        return

    st.markdown("---")
    st.subheader("Opción A — Subir o tomar foto")
    a1, a2 = st.columns(2)
    with a1:
        image_file = st.file_uploader("Imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])
    with a2:
        cam_file = st.camera_input("Tomar foto")

    conf_th = st.slider("Umbral de confianza (visualización)", 0.0, 1.0, 0.0, 0.01)

    candidate_image = None
    if image_file is not None:
        candidate_image = Image.open(image_file).convert("RGB")
    elif cam_file is not None:
        candidate_image = Image.open(cam_file).convert("RGB")

    if candidate_image is not None:
        st.image(candidate_image, caption="Entrada", use_container_width=True)
        if st.button("Predecir"):
            x = preprocess_image(candidate_image, input_hw_c)
            rows = predict_image(model, labels, x, top_k=min(5, len(labels)))
            rows_f = [(lab, prob) for lab, prob in rows if prob >= conf_th] or rows
            st.write({"predicciones": [{"label": lab, "prob": float(prob)} for lab, prob in rows_f]})

    st.markdown("---")
    st.subheader("Opción B — Webcam en tiempo real")
    if not WEBRTC_OK:
        st.info("streamlit-webrtc no disponible en el entorno. Omitido.")
        return

    if st.checkbox("Activar webcam"):
        def factory():
            return _TMVideoTransformer(model, labels, input_hw_c, conf_th)
        webrtc_streamer(
            key="tm-gestos",
            mode=WebRtcMode.SENDRECV,
            video_transformer_factory=factory,
            media_stream_constraints={"video": True, "audio": False},
        )
```
