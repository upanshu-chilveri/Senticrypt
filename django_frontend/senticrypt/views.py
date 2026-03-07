import json
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "senticrypt/index.html")


def _post_to_fastapi(path: str, body: dict):
    """Helper: POST a dict to FastAPI and return (status_code, dict)."""
    url     = f"{settings.FASTAPI_URL}{path}"
    payload = json.dumps(body).encode("utf-8")
    req     = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


@csrf_exempt
def analyse_text(request):
    """Proxy to FastAPI /encrypt — returns emotions + encrypted payload."""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        body = json.loads(request.body)
        text = body.get("text", "").strip()
        if not text:
            return JsonResponse({"error": "Empty text"}, status=400)
        status, data = _post_to_fastapi("/encrypt", {"text": text})
        return JsonResponse(data, status=status)
    except urllib.error.URLError as e:
        return JsonResponse({"error": f"FastAPI unavailable: {e.reason}"}, status=503)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def decrypt_text(request):
    """Proxy to FastAPI /decrypt."""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        body    = json.loads(request.body)
        payload = body.get("payload", "").strip()
        if not payload:
            return JsonResponse({"error": "Empty payload"}, status=400)
        status, data = _post_to_fastapi("/decrypt", {"payload": payload})
        return JsonResponse(data, status=status)
    except urllib.error.URLError as e:
        return JsonResponse({"error": f"FastAPI unavailable: {e.reason}"}, status=503)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
