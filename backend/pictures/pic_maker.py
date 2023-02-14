import os
from datetime import datetime
from pathlib import Path
from random import choice

from PIL import Image
from settings.config import (BACKGROUNDS_DIR, CALENDAR_DIR,
                             COORD_CALENDAR_LEFT_WITH_HORO,
                             COORD_CALENDAR_RIGHT_WITH_HORO,
                             COORD_HOROSCOPE_CENTER, COORD_HOROSCOPE_LEFT,
                             COORD_HOROSCOPE_RIGHT,
                             COORD_PHRASE_LEFT_WITH_HORO,
                             COORD_PHRASE_RIGHT_WITH_HORO, HOROSCOPE_IMG_DIR,
                             IMG_QUALITY, IMG_RESOLUTION, PHRASE_DIR, SUMMER,
                             WINTER, coord_calendar_center,
                             coord_calendar_left, coord_calendar_right,
                             coord_phrase_center, coord_phrase_left,
                             coord_phrase_right)

MONTH = datetime.today().month
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']


class CreateImage:
    def __init__(self):
        self.calendar = Image.new('RGB', IMG_RESOLUTION)
        self.random_background = choice(
            list(Path(BACKGROUNDS_DIR + '/winter').glob('*.*'))
        )
        self.random_phrase = choice(list(Path(PHRASE_DIR).glob('*.*')))
        self.random_calendar = choice(list(Path(CALENDAR_DIR).glob(
            f'*{MONTHS[MONTH - 1]}*.*'))
        )

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

        if zodiac:
            zodiac_img = Image.open(f'{HOROSCOPE_IMG_DIR}{zodiac.lower()}.png')
            if 'left' in self.random_background.name:
                self.calendar.paste(phrase_img, COORD_PHRASE_LEFT_WITH_HORO,
                                    phrase_img)
                self.calendar.paste(calendar_img,
                                    COORD_CALENDAR_LEFT_WITH_HORO,
                                    calendar_img)
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_LEFT,
                                    zodiac_img)
            elif 'right' in self.random_background.name:
                self.calendar.paste(phrase_img, COORD_PHRASE_RIGHT_WITH_HORO,
                                    phrase_img)
                self.calendar.paste(calendar_img,
                                    COORD_CALENDAR_RIGHT_WITH_HORO,
                                    calendar_img)
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_RIGHT,
                                    zodiac_img)
            else:
                self.calendar.paste(phrase_img, coord_phrase_center,
                                    phrase_img)
                self.calendar.paste(calendar_img, coord_calendar_center,
                                    calendar_img)
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_CENTER,
                                    zodiac_img)
        else:
            if 'left' in self.random_background.name:
                self.calendar.paste(phrase_img, coord_phrase_left, phrase_img)
                self.calendar.paste(calendar_img, coord_calendar_left,
                                    calendar_img)
            elif 'right' in self.random_background.name:
                self.calendar.paste(phrase_img, coord_phrase_right, phrase_img)
                self.calendar.paste(calendar_img, coord_calendar_right,
                                    calendar_img)
            else:
                self.calendar.paste(phrase_img, coord_phrase_center,
                                    phrase_img)
                self.calendar.paste(calendar_img, coord_calendar_center,
                                    calendar_img)

        wallpaper_path = os.path.abspath(f'img/{tg_id}.png')
        self.calendar.save(wallpaper_path, quality=IMG_QUALITY)
        return wallpaper_path


if __name__ == '__main__':
    a = CreateImage()
    a.make_wallpaper(1, 'Скорпион')
