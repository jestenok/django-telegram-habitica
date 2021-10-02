import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram_bot.handlers.manager1c import process_1c_event
from telegram_bot.handlers.dispatcher import process_telegram_event
from telegram_bot.handlers.anime import authorize
from telegram_bot.handlers.commands import bot
from telegram_bot.handlers.habitica import task_compleeted
from telegram_bot.handlers.commands import bot_send_message, chat
from telegram_bot.models import User, Logs, Requests
from manager.settings import DEBUG
import telegram
import requests
from manager.config import TG_API_KEY
import socket
from datetime import datetime


def index(request):
    Requests.objects.create(ip_addr=get_client_ip(request), date=datetime.now())
    return render(request, 'index.html')


def chat(request):
    chat(json.loads(request.body))
    return JsonResponse({"ok": "POST request processed"})


@csrf_exempt
def tg(request):
    if request.method == "POST":
        if all([DEBUG,
                request.headers["host"] == "jestenok.ru",
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('jestenok.ru', 8888)) == 0]):
            requests.post(f'http://jestenok.ru:8888/{TG_API_KEY}/', data=request.body)
        else:
            process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})


class Egor:
    def index(request):
        return render(request, 'krasa_winner/index.html')


    def passgen(request):
        return render(request, 'krasa_winner/passGen.html')


    def guess(request):
        return render(request, 'krasa_winner/guess.html')


@csrf_exempt
def anime(request):
    user_id = request.GET.get('user_id')  #user_id = "1021912706"
    u = User.objects.filter(user_id=user_id)
    u.update(anime_code=request.GET.get('code'))
    if authorize(u[0]):
        bot.send_message(text="Аккаунт успешно привязан!",
                         chat_id=user_id,
                         reply_markup=telegram.ReplyKeyboardMarkup(
                             [[telegram.KeyboardButton(text="/task"),
                               telegram.KeyboardButton(text="/search")]],
                         resize_keyboard=True))
    return JsonResponse({"ok": "POST request processed"})


@csrf_exempt
def msg(request):
    if request.method == "POST":
        print(request.body)
        process_1c_event(json.loads(request.body))
        return JsonResponse({"200": "POST request processed"})


@csrf_exempt
def mng(request):
    if request.method == "POST":
        json_string = request.body.decode('utf-8').replace('_id', 'id')
        task_compleeted(json.loads(json_string))
        return JsonResponse({"ok": "POST request processed"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
