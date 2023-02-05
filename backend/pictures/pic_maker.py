from datetime import datetime
from pathlib import Path
import os
from random import choice

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
    WINTER,
    SUMMER,
    IMG_QUALITY,
    IMG_RESOLUTION
)

MONTH = datetime.today().month


class CreateImage:
    def __init__(self):
        self.calendar = Image.new('RGB', IMG_RESOLUTION)
        self.random_background = choice(
            list(Path(BACKGROUNDS_DIR + '/winter').glob('*.*'))
        )
        self.random_phrase = choice(list(Path(PHRASE_DIR).glob('*.*')))
        self.random_calendar = choice(list(Path(CALENDAR_DIR).glob('*february*.*')))

    def get_background(self):
        if MONTH in WINTER:
            return Image.open(self.random_background)
        if MONTH in SUMMER:
            return Image.open(self.random_background)
        return Image.open(self.random_background)

    def get_phrase(self):
        return Image.open(self.random_phrase)

    def get_calendar(self):
        return Image.open(self.random_calendar)

    def make_wallpaper(self, tg_id, zodiac=None):
        phrase_img = self.get_phrase()
        calendar_img = self.get_calendar()
        self.calendar.paste(self.get_background())
        if 'left' in self.random_background.name:
            self.calendar.paste(phrase_img, coord_phrase_left, phrase_img)
            self.calendar.paste(
                calendar_img, coord_calendar_left, calendar_img
            )
        elif 'right' in self.random_background.name:
            self.calendar.paste(phrase_img, coord_phrase_right, phrase_img)
            self.calendar.paste(
                calendar_img, coord_calendar_right, calendar_img
            )
        else:
            self.calendar.paste(phrase_img, coord_phrase_center, phrase_img)
            self.calendar.paste(
                calendar_img, coord_calendar_center, calendar_img
            )

        wallpaper_path = os.path.abspath(f'img/{tg_id}.png')
        self.calendar.save(
            wallpaper_path,
            quality=IMG_QUALITY
        )
        return wallpaper_path


if __name__ == '__main__':
    a = CreateImage()
    a.make_wallpaper(1)
