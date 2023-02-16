from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


# Директории
def get_project_root() -> Path:
    return Path(__file__).parent.parent


ROOT_DIR: str = str(get_project_root())
TEMPLATES_DIR: str = '/templates/'

BACKGROUNDS_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'backgrounds'
PHRASE_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'phrases'
CALENDAR_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'calendars'
MONTHLY_HOROSCOPE_DIR = ROOT_DIR + TEMPLATES_DIR + 'monthly-horoscope/'
HOROSCOPE_IMG_DIR = ROOT_DIR + TEMPLATES_DIR + 'horoscope/'
QUOTES_FILE_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'quotes/quotes.txt'
DAILY_HOROSCOPE_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'daily_horoscope/'


# Координаты для календаря и цитат
coord_phrase_center: tuple = (80, 350)
coord_calendar_center: tuple = (1030, 175)
COORD_HOROSCOPE_CENTER: tuple = (558, 800)

coord_phrase_left: tuple = (1050, 650)
coord_calendar_left: tuple = (1015, 100)
COORD_HOROSCOPE_LEFT: tuple = (1050, 790)
COORD_CALENDAR_LEFT_WITH_HORO = (1050, 45)
COORD_PHRASE_LEFT_WITH_HORO: tuple = (1065, 590)

coord_phrase_right: tuple = (115, 655)
coord_calendar_right: tuple = (90, 95)
COORD_CALENDAR_RIGHT_WITH_HORO = (100, 45)
COORD_HOROSCOPE_RIGHT: tuple = (100, 790)
COORD_PHRASE_RIGHT_WITH_HORO: tuple = (115, 590)

# Времена года
WINTER: tuple = (1, 2, 12)
SUMMER: tuple = (6, 7, 8)

# Настройки создания картинок
IMG_QUALITY: int = 100
IMG_RESOLUTION: tuple = (1920, 1080)

# MongoDB
# MONGO_CLIENT = MongoClient('mongodb://127.0.0.1:27017/')
MONGO_CLIENT = MongoClient('mongodb://mongo_db:27017/')  # server


# Знаки зодиака
ZODIAC_SINGS = {
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
    "pisces": "Рыбы"
}
