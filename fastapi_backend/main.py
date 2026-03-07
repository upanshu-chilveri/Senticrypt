from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# ── Emotion & encryption imports ──────────────────────────────────────────────
from transformers import pipeline, logging as hf_logging
from cryptography.fernet import Fernet
import numpy as np
import json

hf_logging.set_verbosity_error()

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(title="Emotion-Aware Chat API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load emotion model once at startup ────────────────────────────────────────
print("Loading emotion model... (first run downloads ~250 MB)")
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)
print("Emotion model loaded!")

# ── Encryption key (one per server session) ───────────────────────────────────
key    = Fernet.generate_key()
cipher = Fernet(key)


# ── Pydantic models ───────────────────────────────────────────────────────────
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    reply: str
    timestamp: str

class TextInput(BaseModel):
    text: str

class EncryptedInput(BaseModel):
    payload: str


# ── Shared emotion helper ─────────────────────────────────────────────────────
def detect_emotion_embedding(text: str):
    results = emotion_model(text)[0]
    labels  = [r["label"] for r in results]
    scores  = [r["score"] for r in results]
    return labels, np.array(scores)


# ── Chat processing function ──────────────────────────────────────────────────
def process_message(text: str) -> str:
    text  = text.strip()
    lower = text.lower()

    if any(w in lower for w in ["hello", "hi", "hey", "hiya", "howdy"]):
        return "Hey there! Great to hear from you! How can I help today?"
    if any(w in lower for w in ["bye", "goodbye", "see you", "ciao", "later"]):
        return "Goodbye! Come back anytime. Take care!"
    if "how are you" in lower or "how r u" in lower:
        return "I'm doing fantastic, thanks for asking! Ready to chat!"
    if any(q in lower for q in ["what are you", "who are you", "what is this"]):
        return "I'm an emotion-aware chat bot powered by FastAPI + Django! Switch to Emotion Mode to analyse your text."
    if lower in ["help", "?", "help me"]:
        return "Try: 'hello', 'tell me a joke', or switch to Emotion Mode to analyse your text!"
    if "joke" in lower or "funny" in lower:
        return "Why don't scientists trust atoms? Because they make up everything!"
    if "time" in lower or "clock" in lower:
        return f"The current server time is {datetime.now().strftime('%H:%M:%S')}"
    if "date" in lower or "today" in lower:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}"
    if any(w in lower for w in ["thanks", "thank you", "cheers", "awesome", "great"]):
        return "You're very welcome! Happy to help anytime"
    if any(w in lower for w in ["love", "heart"]):
        return "Aww, love right back at ya!"

    words = text.split()
    return (
        f"Got your message! ({len(words)} word{'s' if len(words) != 1 else ''}, {len(text)} chars)\n"
        f"Reversed: \"{' '.join(reversed(words))}\"\n"
        f"Message processed successfully!"
    )


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Emotion-Aware Chat API is running"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/process", response_model=MessageResponse)
def process(req: MessageRequest):
    return MessageResponse(
        reply=process_message(req.message),
        timestamp=datetime.now().isoformat()
    )

@app.post("/encrypt")
def encrypt_text(data: TextInput):
    labels, embedding = detect_emotion_embedding(data.text)
    encrypted_text    = cipher.encrypt(data.text.encode()).decode()
    message           = {
        "ciphertext":        encrypted_text,
        "emotion_embedding": embedding.tolist(),
        "labels":            labels,
    }
    final_encrypted = cipher.encrypt(json.dumps(message).encode()).decode()
    return {
        "encrypted_payload": final_encrypted,
        "emotion_labels":    labels,
        "emotion_embedding": embedding.tolist(),
    }

@app.post("/decrypt")
def decrypt_text(data: EncryptedInput):
    decrypted_payload = cipher.decrypt(data.payload.encode()).decode()
    message           = json.loads(decrypted_payload)
    original_text     = cipher.decrypt(message["ciphertext"].encode()).decode()
    return {
        "original_text":     original_text,
        "emotion_labels":    message["labels"],
        "emotion_embedding": message["emotion_embedding"],
    }
