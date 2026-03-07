from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
from datetime import datetime

app = FastAPI(title="Chat Processor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    reply: str
    timestamp: str


# ── Core processing function ──────────────────────────────────────────────────
def process_message(text: str) -> str:
    """
    Takes an input string and returns a transformed reply.
    Extend this function with any logic you like!
    """
    text = text.strip()
    lower = text.lower()

    # Greetings
    if any(word in lower for word in ["hello", "hi", "hey", "hiya", "howdy"]):
        return "👋 Hey there! Great to hear from you! How can I help today?"

    # Farewells
    if any(word in lower for word in ["bye", "goodbye", "see you", "ciao", "later"]):
        return "👋 Goodbye! Come back anytime. Take care! 🌟"

    # Questions about the bot
    if "how are you" in lower or "how r u" in lower:
        return "😊 I'm doing fantastic, thanks for asking! Ready to chat!"

    # What are you / who are you
    if any(q in lower for q in ["what are you", "who are you", "what is this"]):
        return "🤖 I'm a chat bot powered by FastAPI + Django! Send me any message and I'll respond!"

    # Help
    if lower in ["help", "?", "help me"]:
        return "🆘 Sure! Just type anything and I'll respond. Try: 'hello', 'tell me a joke', or 'what time is it'?"

    # Jokes
    if "joke" in lower or "funny" in lower:
        return "😂 Why don't scientists trust atoms? Because they make up everything! 🧪⚛️"

    # Time
    if "time" in lower or "clock" in lower:
        now = datetime.now().strftime("%H:%M:%S")
        return f"🕐 The current server time is **{now}**"

    # Date
    if "date" in lower or "today" in lower:
        today = datetime.now().strftime("%A, %d %B %Y")
        return f"📅 Today is **{today}**"

    # Compliments
    if any(w in lower for w in ["thanks", "thank you", "cheers", "awesome", "great"]):
        return "😄 You're very welcome! Happy to help anytime 🎉"

    # Love / emoji test
    if any(w in lower for w in ["love", "❤️", "💕", "heart"]):
        return "💖 Aww, love right back at ya! 💕✨"

    # Default: Echo with a twist
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    reversed_words = " ".join(reversed(words))

    return (
        f"📨 Got your message! ({word_count} word{'s' if word_count != 1 else ''}, "
        f"{char_count} chars)\n"
        f"🔄 Reversed: \"{reversed_words}\"\n"
        f"✅ Message processed successfully!"
    )


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "FastAPI Chat Processor is running 🚀"}


@app.get("/health")
def health():
    return {"healthy": True}


@app.post("/process", response_model=MessageResponse)
def process(req: MessageRequest):
    reply = process_message(req.message)
    return MessageResponse(
        reply=reply,
        timestamp=datetime.now().isoformat(),
    )
