import json
from pathlib import Path


SETTINGS_PATH = Path("static/json/app_settings.json")
DEFAULT_LANGUAGE = "uk"
DEFAULT_IMAGE_SET = "default"

LANGUAGE_NAMES = {
    "uk": "Українська",
    "en": "English",
}

IMAGE_SET_FOLDERS = {
    "set_1": Path("media/icons_2"),
    "set_2": Path("media/icons_12hours"),
}

TRANSLATIONS = {
    "uk": {
        "save": "Зберегти",
        "settings": "Налаштування",
        "search": "Пошук",
        "search_city": "Пошук міста",
        "app_size": "Розмір додатку",
        "app_language": "Мова додатку",
        "image_lists": "Списки зображень",
        "images_lists1": "Набір зображень №1",
        "images_lists2": "Набір зображень №2",
        "add": "Додати",
        "choose_app_language": "Оберіть мову додатку",
        "save": "Зберегти",
        "country": "Країна",
        "city": "Місто",
        "coordinates": "Координати",
        "added_cities": "Додані міста",
        "city_not_found": "Місто не знайдено",
        "current_position": "Поточна позиція",
        "today": "Сьогодні",
        "weather_until_end_day": "Погода до кінця дня",
        "forecast_12_hours": "Прогноз на 12 годин",
        "sunrise": "Схід",
        "sunset": "Захід",
        "now": "Зараз",
        "max_min": "Макс.: {max_temp}°, мін.: {min_temp}°",
        "card_max_min": "Макс.: {max_temp}, мін.: {min_temp}",
        "error": "помилка",
        "empty_temperature": "—°",
        "empty_max_min": "Макс.: —, мін.: —",
        "weekday_monday": "Понеділок",
        "weekday_tuesday": "Вівторок",
        "weekday_wednesday": "Середа",
        "weekday_thursday": "Четвер",
        "weekday_friday": "П'ятниця",
        "weekday_saturday": "Субота",
        "weekday_sunday": "Неділя",
    },
    "en": {
        "save": "Save",
        "settings": "Settings",
        "search": "Search",
        "search_city": "City search",
        "app_size": "App size",
        "app_language": "App language",
        "image_lists": "Image lists",
        "images_lists1": "Image set №1",
        "images_lists2": "Image set №2",
        "add": "Add",
        "choose_app_language": "Choose app language",
        "save": "Save",
        "country": "Country",
        "city": "City",
        "coordinates": "Coordinates",
        "added_cities": "Added cities",
        "city_not_found": "City not found",
        "current_position": "Current position",
        "today": "Today",
        "weather_until_end_day": "Weather until end of day",
        "forecast_12_hours": "12-hour forecast",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "now": "Now",
        "max_min": "Max.: {max_temp}°, min.: {min_temp}°",
        "card_max_min": "Max.: {max_temp}, Min.: {min_temp}",
        "error": "error",
        "empty_temperature": "—°",
        "empty_max_min": "Max: —, Min: —",
        "weekday_monday": "Monday",
        "weekday_tuesday": "Tuesday",
        "weekday_wednesday": "Wednesday",
        "weekday_thursday": "Thursday",
        "weekday_friday": "Friday",
        "weekday_saturday": "Saturday",
        "weekday_sunday": "Sunday",
    },
}

WEEKDAY_KEYS = [
    "weekday_monday",
    "weekday_tuesday",
    "weekday_wednesday",
    "weekday_thursday",
    "weekday_friday",
    "weekday_saturday",
    "weekday_sunday",
]


def _read_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_settings(data):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def get_language():
    language = _read_settings().get("language", DEFAULT_LANGUAGE)
    return language if language in TRANSLATIONS else DEFAULT_LANGUAGE


def set_language(language):
    if language not in TRANSLATIONS:
        language = DEFAULT_LANGUAGE

    data = _read_settings()
    data["language"] = language
    _write_settings(data)


def tr(key, **kwargs):
    text = TRANSLATIONS.get(get_language(), TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def weather_api_language():
    return "ua" if get_language() == "uk" else "en"


def weekday_name(date_time):
    return tr(WEEKDAY_KEYS[date_time.weekday()])


def get_image_set():
    image_set = _read_settings().get("image_set", DEFAULT_IMAGE_SET)
    if image_set == DEFAULT_IMAGE_SET or image_set in IMAGE_SET_FOLDERS:
        return image_set
    return DEFAULT_IMAGE_SET


def set_image_set(image_set):
    if image_set != DEFAULT_IMAGE_SET and image_set not in IMAGE_SET_FOLDERS:
        image_set = DEFAULT_IMAGE_SET

    data = _read_settings()
    data["image_set"] = image_set
    _write_settings(data)


def weather_icon_category(weather_id):
    if weather_id is None:
        return 1

    weather_id = int(weather_id)
    if weather_id == 800:
        return 4
    if 200 <= weather_id < 300:
        return 0
    if 300 <= weather_id < 600:
        return 0
    if 600 <= weather_id < 700:
        return 2
    if 700 <= weather_id < 800:
        return 3
    if 801 <= weather_id <= 804:
        return 1
    return 1


def weather_icon_path(default_path, weather_id=None):
    image_set = get_image_set()
    if image_set == DEFAULT_IMAGE_SET:
        return default_path

    folder = IMAGE_SET_FOLDERS[image_set]
    if image_set == "set_1":
        if weather_id is None:
            return default_path
        category = weather_icon_category(weather_id)
        if category == 0:
            icon_name = "Weather Icon.svg"
        else:
            icon_name = f"Weather Icon-{category}.svg"
        custom_path = folder / icon_name
    else:  # set_2
        custom_path = folder / Path(default_path).name
    return str(custom_path) if custom_path.exists() else default_path
