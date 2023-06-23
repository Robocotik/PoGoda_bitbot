import json

import requests
from bs4 import BeautifulSoup

url = "https://www.gismeteo.ru/catalog/"
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
soup = BeautifulSoup(response.text, "lxml")

all_warps = {i.text: i.get("href") for i in soup.find(class_="catalog-list").find_all(class_="popular-city")}
with open("city_catalog.json", "w", encoding="utf-8") as file:
    json.dump(all_warps, file, indent=4, ensure_ascii=False)
