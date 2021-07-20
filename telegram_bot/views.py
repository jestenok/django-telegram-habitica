import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from telegram_bot.handlers.dispatcher import process_telegram_event
from telegram_bot.handlers.anime import authorize
import os
import requests


def index(request):
    return JsonResponse({"error": "sup hacker"})


@csrf_exempt
def tg(request):
    if request.method == "POST":
        print(request.body)
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

def yandex(request):
    return render(request, '/home/django-telegram-habitica/telegram_bot/templates/yandex_3aea5109bc205283.html')


@csrf_exempt
def anime(request):
    authorize("1021912706", request.GET.get('code'))
    return JsonResponse({"ok": "POST request processed"})