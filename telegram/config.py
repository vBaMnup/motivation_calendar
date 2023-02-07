import os
from dotenv import load_dotenv

load_dotenv()

BOT_API_KEY = os.environ.get('BOT_API_KEY')
API_DOMEN = os.environ.get('API_DOMEN')
USER_CREATE_API = os.environ.get('USER_CREATE_API')
CREATE_CALENDAR_API = os.environ.get('CREATE_CALENDAR_API')
MONTHLY_HOROSCOPE_API = os.environ.get('MONTHLY_HOROSCOPE_API')
