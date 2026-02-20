import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from chatapp.services import QwenChatService

chat_service = QwenChatService()


@require_GET
def index(request):
    return render(
        request,
        'chatapp/index.html',
        {'message': 'MazoonAI Django App', 'model': chat_service.model_name},
    )


@require_GET
def health(request):
    return JsonResponse({'status': 'ok', 'framework': 'Django', 'model': chat_service.model_name})


@csrf_exempt
@require_POST
def chat(request):
    try:
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid JSON body'}, status=400)

    message = (payload.get('message') or '').strip()
    history = payload.get('history') or []

    if not message:
        return JsonResponse({'error': 'message is required'}, status=400)

    try:
        answer = chat_service.chat(message, history)
    except RuntimeError as exc:
        return JsonResponse(
            {
                'error': str(exc),
                'hint': 'Install dependencies and run once to download Qwen model.',
            },
            status=503,
        )

    return JsonResponse({'reply': answer, 'model': chat_service.model_name})
