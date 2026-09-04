
import re 
import unicodedata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ------------------------------------------------------------
# Cấu hình
# ------------------------------------------------------------
MODEL_PATH = "./phobert_fakenews_final"   # thư mục model bạn vừa tải về
MAX_LEN = 256
LABEL_NAMES = {0: "An toàn", 1: "Độc hại (Tin giả / Lừa đảo)"}

app = FastAPI(title="API Phát hiện Tin giả & Lừa đảo — PhoBERT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Đang load model từ {MODEL_PATH} lên {device} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
model.eval()
print("✅ Model đã sẵn sàng.")

try:
    import py_vncorenlp
    rdrsegmenter = py_vncorenlp.VnCoreNLP(save_dir="./vncorenlp")
    HAS_SEGMENTER = True
except Exception as e:
    print("⚠️  Không load được VnCoreNLP, sẽ bỏ qua bước tách từ:", e)
    HAS_SEGMENTER = False


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text))
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    emoji_pattern = re.compile(
        "[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F1E6-\U0001F1FF" "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def segment(text: str) -> str:
    if not HAS_SEGMENTER:
        return text
    try:
        return " ".join(rdrsegmenter.word_segment(text))
    except Exception:
        return text

class TextInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    label: int
    label_name: str
    confidence: float
    probabilities: dict


@app.get("/")
def root():
    return {"status": "ok", "message": "API Phát hiện Tin giả & Lừa đảo (PhoBERT) đang chạy."}


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: TextInput):
    cleaned = clean_text(input_data.text)
    segmented = segment(cleaned)

    inputs = tokenizer(
        segmented, truncation=True, padding="max_length",
        max_length=MAX_LEN, return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    pred_label = int(probs.argmax())

    return PredictionOutput(
        label=pred_label,
        label_name=LABEL_NAMES[pred_label],
        confidence=float(probs[pred_label]),
        probabilities={"An toàn": float(probs[0]), "Độc hại": float(probs[1])},
    )
