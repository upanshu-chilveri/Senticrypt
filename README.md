# 💬 ChatApp — FastAPI + Django

A beautiful cream-coloured chat application where Django serves the frontend and FastAPI handles message processing.

## Architecture

```
Browser → Django (port 8000) → FastAPI (port 8001)
                                    ↓
                           process_message(str) → str
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start both servers (Linux/macOS)
chmod +x start.sh
./start.sh

# Or start manually in two terminals:

# Terminal 1 — FastAPI backend
cd fastapi_backend
uvicorn main:app --port 8001 --reload

# Terminal 2 — Django frontend
cd django_frontend
python manage.py runserver 8000
```

Open **http://127.0.0.1:8000** in your browser.

## Customising the Processing Function

Edit `fastapi_backend/main.py` → `process_message(text: str) -> str`

The function receives the user's input string and must return a reply string.
All the routing, templating, and UI glue is handled for you.

## Project Structure

```
chat_app/
├── requirements.txt
├── start.sh
├── fastapi_backend/
│   └── main.py          ← FastAPI app + process_message()
└── django_frontend/
    ├── manage.py
    ├── django_frontend/
    │   ├── settings.py
    │   └── urls.py
    └── chatapp/
        ├── views.py     ← proxies to FastAPI
        ├── urls.py
        └── templates/
            └── chatapp/
                └── index.html  ← cream chat UI
```

## Features

- 🎨 Cream-coloured UI with warm brown accents
- 😊 Built-in emoji picker
- ⌨️ Shift+Enter for newlines, Enter to send
- 💬 Typing indicator animation
- 🔄 Auto-resizing textarea
- 📱 Responsive design
- ⚡ FastAPI async backend
