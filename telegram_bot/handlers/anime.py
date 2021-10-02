import json
from collections import namedtuple
from telegram_bot.models import User, Logs
import requests
from pprint import pprint
from manager.config import anime_client_id, anime_client_secret


def anime_headers(token = ""):
    headers = {"User-Agent": "telegram bot", "Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def search(u, text="", planned=False, retry=True):
    params = {"q": f"{text}"}
    if planned:
        params["mylist"] = "planned"
        params["limit"] = "50"
    else:
        params["limit"] = "10"

    r = requests.get("https://shikimori.one/api/animes",
                     params=params,
                     headers=anime_headers(u.anime_token))

    if r.status_code == 200:
        json_data = json.dumps(r.json())
        return json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    elif r.status_code == 401 and retry:
        if authorize(u):
            return search(u, text, planned, False)


def change_status(u, id, status):
    data = {
        "user_rate": {
            "target_id": id,
            "status": status,
            "target_type": "Anime",
            "user_id": u.anime_id
        }
    }

    r = requests.post("https://shikimori.one/api/v2/user_rates",
                      headers=anime_headers(u.anime_token),
                      json=data)


def authorize(u):
    success = False

    data = {
        "client_id":anime_client_id,
        "client_secret":anime_client_secret,
    }

    if u.anime_refresh_token:
        data["grant_type"] = "refresh_token"
        data["refresh_token"] = u.anime_refresh_token
    else:
        data["grant_type"] = "authorization_code"
        data["code"] = u.anime_code
        data["redirect_uri"] = f"https://jestenok.ru/anime?user_id={u.user_id}"

    print(data)
    r = requests.post(url="https://shikimori.one/oauth/token",
                            headers=anime_headers(),
                            allow_redirects=False,
                            json=data)

    Logs.log("Авторизация шики", u, r.content)
    if r.status_code == 200:
        token = json.loads(r.content)['access_token']
        r_whoami = requests.get(url="https://shikimori.one/api/users/whoami",
                                headers=anime_headers(token))

        Logs.log("Получаем код", u, r_whoami.status_code)
        if r_whoami.status_code == 200:
            User.objects.filter(user_id=u.user_id).update(anime_token=token,
                                                          anime_refresh_token=json.loads(r.content)['refresh_token'],
                                                          anime_id=json.loads(r_whoami.content)['id'],
                                                          anime=True)
            success = True

    return success
