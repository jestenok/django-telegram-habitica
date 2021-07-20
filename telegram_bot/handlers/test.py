# import requests
# import json
# from collections import namedtuple
#
#
# headers={"User-Agent": "telegram bot", "Content-Type":"application/json"}
#
#
# def search(token, text):
#     headers["Authorization"] = f"Bearer {token}"
#     r = requests.get("https://shikimori.one/api/animes",
#                       params={"q":f"{text}", "limit":"10"},
#                       headers=headers)
#
#     json_data = json.dumps(r.json())
#     obj = json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
#
#     for item in obj:
#
#     return r.json()
#
#
# search("LeRmfurT5dXGs3CCCuleTp1zcXSrZce5ma_0rxo51w4", "Гуль")