import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from telegram_bot.handlers.dispatcher import process_telegram_event
from telegram_bot.handlers.anime import authorize
from telegram_bot.handlers.commands import send_message_to_admin
import wdb
import os
import requests

from telegram_bot.models import User, Logs


def index(request):
    return JsonResponse({"error": "sup hacker"})


@csrf_exempt
def tg(request):
    if request.method == "POST":
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

def yandex(request):
    return render(request, '/home/django-telegram-habitica/telegram_bot/templates/yandex_3aea5109bc205283.html')


class Egor:
    def index(request):
        return render(request, '/home/django-telegram-habitica/telegram_bot/templates/krasa_winner/index.html')


    def passgen(request):
        return render(request, '/home/django-telegram-habitica/telegram_bot/templates/krasa_winner/passGen.html')


    def guess(request):
        return render(request, '/home/django-telegram-habitica/telegram_bot/templates/krasa_winner/guess.html')


@csrf_exempt
def anime(request):
    u = User.objects.filter(user_id="1021912706")
    u.update(anime_code=request.GET.get('code'))
    authorize(u[0])
    return JsonResponse({"ok": "POST request processed"})