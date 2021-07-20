import json
from collections import namedtuple
from telegram_bot.models import User
import requests
from pprint import pprint
from manager.config import anime_client_id, anime_client_secret
import web_pdb


headers={"User-Agent": "telegram bot", "Content-Type":"application/json"}


def search(token, text):
    headers["Authorization"] = f"Bearer {token}"
    r = requests.get("https://shikimori.one/api/animes",
                      params={"q":f"{text}", "limit":"10"},
                      headers=headers)

    json_data = json.dumps(r.json())
    return json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def authorize(user_id, code):
    u = User.objects.filter(user_id=user_id)
    u.update(anime_code=code)

    data = {
    "grant_type":"authorization_code",
    "client_id":anime_client_id,
    "client_secret":anime_client_secret,
    "code":code,
    "redirect_uri":f"https://jestenok.ru/anime"
    }

    response = requests.post(url="https://shikimori.one/oauth/token",
                            headers=headers,
                            allow_redirects=False,
                            json=data)

    if response.status_code == 200:
        u.update(anime_token=response.json()['access_token'],
                 anime_refresh_token=response.json()['refresh_token'],
                 anime=True)
