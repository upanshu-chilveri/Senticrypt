#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  start.sh  –  Launch FastAPI (port 8001) + Django (port 8000)
#  Works with paths that contain spaces.
# ──────────────────────────────────────────────────────────────

# Resolve the directory this script lives in (handles spaces)
SCRIPT_PATH="${BASH_SOURCE[0]}"
ROOT="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd)"

FASTAPI_DIR="${ROOT}/fastapi_backend"
DJANGO_DIR="${ROOT}/django_frontend"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║   ChatApp  –  FastAPI + Django        ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  Root: ${ROOT}"
echo ""

# ── Sanity checks ─────────────────────────────────────────────
if [ ! -d "${FASTAPI_DIR}" ]; then
  echo "  ❌  ERROR: Cannot find fastapi_backend at:"
  echo "      ${FASTAPI_DIR}"
  echo ""
  echo "  Make sure start.sh is in the same folder as"
  echo "  fastapi_backend/ and django_frontend/"
  exit 1
fi

if [ ! -d "${DJANGO_DIR}" ]; then
  echo "  ❌  ERROR: Cannot find django_frontend at:"
  echo "      ${DJANGO_DIR}"
  exit 1
fi

# ── 1. Install dependencies ───────────────────────────────────
echo "📦  Installing dependencies…"
pip install -r "${ROOT}/requirements.txt" -q
echo "  ✅  Dependencies ready"
echo ""

# ── 2. Start FastAPI ──────────────────────────────────────────
echo "🚀  Starting FastAPI backend  →  http://127.0.0.1:8001"
(cd "${FASTAPI_DIR}" && uvicorn main:app --host 127.0.0.1 --port 8001 --reload) &
FASTAPI_PID=$!

# ── 3. Wait for FastAPI to boot ───────────────────────────────
sleep 2

# ── 4. Start Django ───────────────────────────────────────────
echo "🌐  Starting Django frontend  →  http://127.0.0.1:8000"
(cd "${DJANGO_DIR}" && python manage.py runserver 127.0.0.1:8000) &
DJANGO_PID=$!

echo ""
echo "  ✅  Both servers are running!"
echo "  🌍  Open your browser:  http://127.0.0.1:8000"
echo ""
echo "  Press Ctrl+C to stop both servers."
echo ""

# ── Cleanup on exit ───────────────────────────────────────────
cleanup() {
  echo ""
  echo "  Stopping servers…"
  kill "${FASTAPI_PID}" "${DJANGO_PID}" 2>/dev/null
  wait "${FASTAPI_PID}" "${DJANGO_PID}" 2>/dev/null
  echo "  👋  Goodbye!"
  exit 0
}

trap cleanup SIGINT SIGTERM

wait
