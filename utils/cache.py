import json
import time
from pathlib import Path

from .api_request import api_request
from .i18n import get_language


CACHE_DIR = Path("static/json/weather_cache")
CACHE_TTL = 15 * 60  

def get_cache_file_path(city_name):
    safe_name = city_name.strip().lower().replace(" ", "_")
    full_path = Path(f"static/json/weather_cache/{safe_name}_{get_language()}.json")
    return full_path


def get_weather(city_name):

    cache_file = get_cache_file_path(city_name)

    
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        cache_age = time.time() - saved_data["timestamp"]

       
        if cache_age < CACHE_TTL:
            if saved_data["data"].get("cod") == "200":
                return saved_data["data"]
            else:
                print(f"Кэш содержит ошибку, запрашиваем заново")

    print(f"Запрос к API для города: {city_name}")
    data = api_request(city_name)

    if data.get("cod") == "200":
        entry = {
            "timestamp": time.time(),  
            "data": data               
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

        print(f"Сохранено в кэш: {cache_file.name}")
    return data

def get_cached_cities():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cities = []
    seen_cities = set()

    for file in CACHE_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if data["data"].get("cod") == "200":
                city_name = data["data"]["city"]["name"]
                city_key = city_name.strip().lower()
                if city_key not in seen_cities:
                    cities.append(city_name)
                    seen_cities.add(city_key)

        except Exception as e:
            print(f"Ошибка чтения {file}: {e}")

    return cities

def remove_cached_city(city_name):
    safe_name = city_name.strip().lower().replace(" ", "_")
    for cache_file in CACHE_DIR.glob(f"{safe_name}*.json"):
        cache_file.unlink()  # удаляет файл
        print(f"Удалён кэш: {cache_file.name}")
