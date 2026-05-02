import requests
import json

import dotenv
import os
from .i18n import weather_api_language

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

CITY_ALIAS = {
    "мюнхен": "Munich",
    "munich": "Munich",
    "muenchen": "Munich",
}


def api_request(city_name: str):
    normalized = city_name.strip()
    low = normalized.lower()

    if low in CITY_ALIAS:
        normalized = CITY_ALIAS[low]

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?q={normalized}&units=metric&lang={weather_api_language()}&appid={API_KEY}",
        timeout=15,
    )

    data_dict = response.json()

    if data_dict.get("cod") != "200":
        # Возвращаем данные с ошибкой, чтобы не добавлять карту
        return {"cod": "404", "message": "City not found"}


    with open("static/json/city_data.json", mode="w", encoding="utf-8") as file:
        json.dump(data_dict, file, ensure_ascii=False, indent=4)

    return data_dict

def api_request_no_file(city_name: str):
    normalized = city_name.strip()
    low = normalized.lower()

    if low in CITY_ALIAS:
        normalized = CITY_ALIAS[low]

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?q={normalized}&units=metric&lang={weather_api_language()}&appid={API_KEY}",
        timeout=15,
    )

    data_dict = response.json()

    if data_dict.get("cod") != "200":
        return {"cod": "404", "message": "City not found"}

    return data_dict


def city_request():
    response = requests.get("https://ipinfo.io/json")
    data_dict = response.json()

    return data_dict.get("city", "Dnipro")



# response = requests.get("https://countriesnow.space/api/v0.1/countries/population/cities")
# data_dict = response.json()
# with open("static/json/cities.json", mode="w", encoding="utf-8") as file:
#     json.dump(data_dict, file, ensure_ascii=False, indent=4)
