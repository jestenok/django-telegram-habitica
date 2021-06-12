import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram_bot.handlers.dispatcher import process_telegram_event


def index(request):
    return JsonResponse({"error": "sup hacker"})


@csrf_exempt
def tg(request):
    if request.method == "POST":
        print(request.body)
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

