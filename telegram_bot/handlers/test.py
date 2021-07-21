import requests

headers={"User-Agent": "telegram bot", "Content-Type":"application/json"}
print(requests.get(f"https://shikimori.one/system/animes/original/22319.jpg?1610272095", headers=headers).content)