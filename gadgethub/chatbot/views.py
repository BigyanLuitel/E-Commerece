import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json


@login_required
@require_POST
def chat_send(request):
    try:
        payload = json.loads(request.body)
        user_message = payload.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request"}, status=400)

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    history = request.session.get("chat_history", [])
    history.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            f"{settings.AI_SERVICE_URL}/chat/",
            json={"user_id": request.user.id, "messages": history},
            timeout=30,
        )
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text
            return JsonResponse({"error": f"Assistant error: {detail}"}, status=502)
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": f"Assistant is unavailable: {str(e)}"}, status=502)

    history.append({"role": "assistant", "content": data["reply"]})
    request.session["chat_history"] = history
    request.session.modified = True

    return JsonResponse({
        "reply": data["reply"],
        "payment_qr_base64": data.get("payment_qr_base64"),
        "payment_url": data.get("payment_url"),
    })


@login_required
@require_POST
def chat_reset(request):
    request.session["chat_history"] = []
    request.session.modified = True
    return JsonResponse({"success": True})


@login_required
def chat_history(request):
    return JsonResponse({"history": request.session.get("chat_history", [])})