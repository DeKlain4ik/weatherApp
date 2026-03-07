import json
import time
from pathlib import Path

from .api_request import api_request


CACHE_DIR = Path("static/json/weather_cache")
CACHE_TTL = 15 * 60  

def get_cache_file_path(city_name):
    safe_name = city_name.strip().lower().replace(" ", "_")
    full_path = Path(f"static/json/weather_cache/{safe_name}.json")
    return full_path


def get_weather(city_name):

    cache_file = get_cache_file_path(city_name)

    
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        cache_age = time.time() - saved_data["timestamp"]

       
        if cache_age < CACHE_TTL:
            return saved_data["data"]
        else:
            print(f"Кэш устарел, запрашиваем заново")

    print(f"Запрос к API для города: {city_name}")
    data = api_request(city_name)

    entry = {
        "timestamp": time.time(),  
        "data": data               
    }

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)

    print(f"Сохранено в кэш: {cache_file.name}")
    return data