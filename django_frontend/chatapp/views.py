import json
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Render the main chat UI."""
    return render(request, "chatapp/index.html")


@csrf_exempt
def send_message(request):
    """Proxy message to FastAPI and return the response."""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get("message", "").strip()
        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Forward to FastAPI
    fastapi_url = f"{settings.FASTAPI_URL}/process"
    payload = json.dumps({"message": message}).encode("utf-8")

    try:
        req = urllib.request.Request(
            fastapi_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return JsonResponse(data)
    except urllib.error.URLError as e:
        return JsonResponse(
            {"error": f"FastAPI backend unavailable: {e.reason}"},
            status=503,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
