import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

BOT_API_KEY = os.environ.get('BOT_API_KEY')
API_DOMEN = os.environ.get('API_DOMEN')
USER_CREATE_API = os.environ.get('USER_CREATE_API')
CREATE_CALENDAR_API = os.environ.get('CREATE_CALENDAR_API')
MONTHLY_HOROSCOPE_API = os.environ.get('MONTHLY_HOROSCOPE_API')
SUBSCRIBE_API = os.environ.get('SUBSCRIBE_API')
SUBSCRIBE_QUOTES_API = os.environ.get('SUBSCRIBE_QUOTES_API')
GET_DAILY_QUOTES_API = os.environ.get('GET_DAILY_QUOTES_API')
GET_ALL_SUBSCRIBER_API = os.environ.get('GET_ALL_SUBSCRIBER')

WELCOME_MESSAGE = (
    "Привет, нажми на создать календарь или добавь знак зодиака, "
    "чтобы получить гороскоп на месяц или создать календарь с гороскопом. "
    "Платные подписчики могут смотреть гороскопы для других знаков зодиака, "
    "получать ежедневные гороскопы и мотивационные цитаты")


bot = Bot(BOT_API_KEY)
dp = Dispatcher(bot)
