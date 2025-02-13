from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


# Директории
def get_project_root() -> Path:
    return Path(__file__).parent.parent


ROOT_DIR: str = str(get_project_root())
TEMPLATES_DIR: str = "/templates/"

BACKGROUNDS_DIR: str = ROOT_DIR + TEMPLATES_DIR + "backgrounds"
PHRASE_DIR: str = ROOT_DIR + TEMPLATES_DIR + "phrases"
CALENDAR_DIR: str = ROOT_DIR + TEMPLATES_DIR + "calendars"
MONTHLY_HOROSCOPE_DIR = ROOT_DIR + TEMPLATES_DIR + "monthly-horoscope/"
HOROSCOPE_IMG_DIR = ROOT_DIR + TEMPLATES_DIR + "horoscope/"
QUOTES_FILE_DIR: str = ROOT_DIR + TEMPLATES_DIR + "quotes/quotes.txt"
FONTS_DIR: str = ROOT_DIR + TEMPLATES_DIR + "fonts/"
DAILY_HOROSCOPE_DIR: str = ROOT_DIR + TEMPLATES_DIR + "daily_horoscope/"


# Координаты для календаря и цитат
COORD_PHRASE_CENTER: tuple = (40, 350)
COORD_CALENDAR_CENTER: tuple = (1030, 175)
COORD_HOROSCOPE_CENTER: tuple = (553, 800)

COORD_PHRASE_LEFT: tuple = (1035, 650)
COORD_CALENDAR_LEFT: tuple = (1015, 100)
COORD_HOROSCOPE_LEFT: tuple = (1005, 790)
COORD_CALENDAR_LEFT_WITH_HORO = (1020, 45)
COORD_PHRASE_LEFT_WITH_HORO: tuple = (0, 590)

COORD_PHRASE_RIGHT: tuple = (110, 655)
COORD_CALENDAR_RIGHT: tuple = (90, 95)
COORD_CALENDAR_RIGHT_WITH_HORO = (60, 45)
COORD_HOROSCOPE_RIGHT: tuple = (45, 790)
COORD_PHRASE_RIGHT_WITH_HORO: tuple = (0, 590)

# Времена года
WINTER: tuple = (1, 2, 12)
SUMMER: tuple = (6, 7, 8)

# Настройки создания картинок
IMG_QUALITY: int = 90
IMG_RESOLUTION: tuple = (1920, 1080)

# MongoDB
MONGO_CLIENT = MongoClient("mongodb://127.0.0.1:27017/")
# MONGO_CLIENT = MongoClient("mongodb://mongo_db:27017/")  # server


# Знаки зодиака
ZODIAC_SIGNS = {
    "aries": "Овен",
    "taurus": "Телец",
    "gemini": "Близнецы",
    "cancer": "Рак",
    "leo": "Лев",
    "virgo": "Дева",
    "libra": "Весы",
    "scorpio": "Скорпион",
    "sagittarius": "Стрелец",
    "capricorn": "Козерог",
    "aquarius": "Водолей",
    "pisces": "Рыбы",
}

# Настройки текста
TEXT_SHADOW_OFFSET = 2  # Смещение тени текста в пикселях
FONT_SIZE_REGULAR = 40  # Размер обычного шрифта
FONT_SIZE_SMALL = 35  # Размер уменьшенного шрифта
LINE_SPACING = 5  # Межстрочный интервал

# Координаты элементов для разных позиций (x, y)
COORD_MAP = {
    "left": {
        "phrase": COORD_PHRASE_LEFT,
        "calendar": COORD_CALENDAR_LEFT,
        "zodiac": COORD_HOROSCOPE_LEFT,
        "calendar_with_horo": COORD_CALENDAR_LEFT_WITH_HORO,
        "phrase_with_horo": COORD_PHRASE_LEFT_WITH_HORO,
    },
    "right": {
        "phrase": COORD_PHRASE_RIGHT,
        "calendar": COORD_CALENDAR_RIGHT,
        "zodiac": COORD_HOROSCOPE_RIGHT,
        "calendar_with_horo": COORD_CALENDAR_RIGHT_WITH_HORO,
        "phrase_with_horo": COORD_PHRASE_RIGHT_WITH_HORO,
    },
    "center": {
        "phrase": COORD_PHRASE_CENTER,
        "calendar": COORD_CALENDAR_CENTER,
        "zodiac": COORD_HOROSCOPE_CENTER,
    },
}


# Координаты для календаря и цитат на экране MacBook (16:10)
COORD_PHRASE_CENTER_MAC = (0, 400)
COORD_CALENDAR_CENTER_MAC = (1100, 200)
COORD_HOROSCOPE_CENTER_MAC = (600, 900)

COORD_PHRASE_LEFT_MAC = (1000, 700)
COORD_CALENDAR_LEFT_MAC = (1100, 150)
COORD_HOROSCOPE_LEFT_MAC = (1100, 900)
COORD_CALENDAR_LEFT_WITH_HORO_MAC = (1100, 100)
COORD_PHRASE_LEFT_WITH_HORO_MAC = (0, 650)

COORD_PHRASE_RIGHT_MAC = (100, 700)
COORD_CALENDAR_RIGHT_MAC = (150, 150)
COORD_CALENDAR_RIGHT_WITH_HORO_MAC = (100, 100)
COORD_HOROSCOPE_RIGHT_MAC = (100, 900)
COORD_PHRASE_RIGHT_WITH_HORO_MAC = (0, 650)

# Обновленный словарь COORD_MAP для MacBook
COORD_MAP_MAC = {
    "left": {
        "phrase": COORD_PHRASE_LEFT_MAC,
        "calendar": COORD_CALENDAR_LEFT_MAC,
        "zodiac": COORD_HOROSCOPE_LEFT_MAC,
        "calendar_with_horo": COORD_CALENDAR_LEFT_WITH_HORO_MAC,
        "phrase_with_horo": COORD_PHRASE_LEFT_WITH_HORO_MAC,
    },
    "right": {
        "phrase": COORD_PHRASE_RIGHT_MAC,
        "calendar": COORD_CALENDAR_RIGHT_MAC,
        "zodiac": COORD_HOROSCOPE_RIGHT_MAC,
        "calendar_with_horo": COORD_CALENDAR_RIGHT_WITH_HORO_MAC,
        "phrase_with_horo": COORD_PHRASE_RIGHT_WITH_HORO_MAC,
    },
    "center": {
        "phrase": COORD_PHRASE_CENTER_MAC,
        "calendar": COORD_CALENDAR_CENTER_MAC,
        "zodiac": COORD_HOROSCOPE_CENTER_MAC,
    },
}
