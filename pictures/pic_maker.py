import random
from datetime import datetime
from pathlib import Path

from PIL import Image

from settings.config import BACKGROUNDS_DIR, PHRASE_DIR, CALENDAR_DIR

# Путь к текущему файлу
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MONTH = datetime.today().month

coord_phrase_center = (80, 350)
coord_calendar_center = (1030, 175)

coord_phrase_left = (1050, 650)
coord_calendar_left = (1015, 100)

coord_phrase_right = (115, 655)
coord_calendar_right = (90, 95)

if MONTH in [1, 2, 12]:
    random_background = random.choice(list(Path(BACKGROUNDS_DIR + '/winter').glob('*.*')))
elif MONTH in [6, 7, 8]:
    random_background = random.choice(list(Path(BACKGROUNDS_DIR + '/summer').glob('*.*')))
else:
    random_background = random.choice(list(Path(BACKGROUNDS_DIR).glob('*.*')))
random_phrase = random.choice(list(Path(PHRASE_DIR).glob('*.*')))
random_calendar = random.choice(list(Path(CALENDAR_DIR).glob('*.*')))

calendar = Image.new('RGB', (1920, 1080))
back_image = Image.open(random_background)
phrase_img = Image.open(random_phrase)
calendar_img = Image.open(random_calendar)


calendar.paste(back_image)
if 'left' in random_background.name:
    calendar.paste(phrase_img, coord_phrase_left, phrase_img)
    calendar.paste(calendar_img, coord_calendar_left, calendar_img)
elif 'right' in random_background.name:
    calendar.paste(phrase_img, coord_phrase_right, phrase_img)
    calendar.paste(calendar_img, coord_calendar_right, calendar_img)
else:
    calendar.paste(phrase_img, coord_phrase_center, phrase_img)
    calendar.paste(calendar_img, coord_calendar_center, calendar_img)

calendar.save('1.png', quality=100)
