import requests
import json

from config import API_KEY


def api_request(city_name: str):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}")
    data_dict = response.json()

    with open("static/json/city_data.json", mode = "w") as file:
        cnt = json.dumps(data_dict, indent=4, ensure_ascii=False)
        file.write(cnt)
    
    return data_dict


def city_request():
    response = requests.get("https://ipinfo.io/json")
    data_dict = response.json()

    return data_dict["city"]



