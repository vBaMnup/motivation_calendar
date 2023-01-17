from random import choice
from datetime import datetime
from pathlib import Path

from PIL import Image

from settings.config import (
    BACKGROUNDS_DIR,
    PHRASE_DIR,
    CALENDAR_DIR,
    coord_phrase_left,
    coord_calendar_left,
    coord_phrase_right,
    coord_calendar_right,
    coord_phrase_center,
    coord_calendar_center,
    winter,
    summer
)

# Путь к текущему файлу
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MONTH = datetime.today().month


class CreateImage:
    def __init__(self):
        self.calendar = Image.new('RGB', (1920, 1080))
        self.random_background = choice(
            list(Path(BACKGROUNDS_DIR + '/winter').glob('*.*'))
        )
        self.random_phrase = choice(list(Path(PHRASE_DIR).glob('*.*')))
        self.random_calendar = choice(list(Path(CALENDAR_DIR).glob('*.*')))

    def get_background(self):
        if MONTH in winter:
            return Image.open(self.random_background)
        if MONTH in summer:
            return Image.open(self.random_background)
        return Image.open(self.random_background)

    def get_phrase(self):
        return Image.open(self.random_phrase)

    def get_calendar(self):
        return Image.open(self.random_calendar)

    def make_wallpaper(self):
        phrase_img = self.get_phrase()
        calendar_img = self.get_calendar()
        self.calendar.paste(self.get_background())
        if 'left' in self.random_background.name:
            self.calendar.paste(phrase_img, coord_phrase_left, phrase_img)
            self.calendar.paste(calendar_img, coord_calendar_left, calendar_img)
        elif 'right' in self.random_background.name:
            self.calendar.paste(phrase_img, coord_phrase_right, phrase_img)
            self.calendar.paste(calendar_img, coord_calendar_right, calendar_img)
        else:
            self.calendar.paste(phrase_img, coord_phrase_center, phrase_img)
            self.calendar.paste(calendar_img, coord_calendar_center, calendar_img)

        self.calendar.save('test.png', quality=100)


a = CreateImage()
a.make_wallpaper()
