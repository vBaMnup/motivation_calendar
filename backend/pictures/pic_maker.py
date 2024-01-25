import os
import random
from datetime import datetime
from pathlib import Path
from random import choice
from typing import List

from PIL import Image, ImageDraw, ImageFont
from pictures.string_split import (
    get_text_from_json,
    make_strings_from_text,
    get_key_by_dict,
)

from settings.config import (
    BACKGROUNDS_DIR,
    CALENDAR_DIR,
    COORD_CALENDAR_LEFT_WITH_HORO,
    COORD_CALENDAR_RIGHT_WITH_HORO,
    COORD_HOROSCOPE_CENTER,
    COORD_HOROSCOPE_LEFT,
    COORD_HOROSCOPE_RIGHT,
    COORD_PHRASE_LEFT_WITH_HORO,
    COORD_PHRASE_RIGHT_WITH_HORO,
    HOROSCOPE_IMG_DIR,
    IMG_QUALITY,
    IMG_RESOLUTION,
    PHRASE_DIR,
    SUMMER,
    WINTER,
    ZODIAC_SINGS,
    COORD_CALENDAR_CENTER,
    COORD_CALENDAR_LEFT,
    COORD_CALENDAR_RIGHT,
    COORD_PHRASE_CENTER,
    COORD_PHRASE_LEFT,
    COORD_PHRASE_RIGHT,
    FONTS_DIR,
    QUOTES_FILE_DIR,
)

MONTH = datetime.today().month
MONTHS = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]
COORDS = {
    "left": {
        "phrase": COORD_PHRASE_LEFT,
        "calendar": COORD_CALENDAR_LEFT,
        "phrase_with_horo": COORD_PHRASE_LEFT_WITH_HORO,
        "calendar_with_horo": COORD_CALENDAR_LEFT_WITH_HORO,
        "zodiac": COORD_HOROSCOPE_LEFT,
    },
    "right": {
        "phrase": COORD_PHRASE_RIGHT,
        "calendar": COORD_CALENDAR_RIGHT,
        "phrase_with_horo": COORD_PHRASE_RIGHT_WITH_HORO,
        "calendar_with_horo": COORD_CALENDAR_RIGHT_WITH_HORO,
        "zodiac": COORD_HOROSCOPE_RIGHT,
    },
    "center": {
        "phrase": COORD_PHRASE_CENTER,
        "calendar": COORD_CALENDAR_CENTER,
        "zodiac": COORD_HOROSCOPE_CENTER,
    },
}


class CreateImage:
    def __init__(self):
        self.calendar = Image.new("RGB", IMG_RESOLUTION)
        if MONTH in WINTER:
            backgrounds = list(Path(BACKGROUNDS_DIR + "/winter").glob("*.*"))
        else:
            backgrounds = list(Path(BACKGROUNDS_DIR).glob("*.*"))
        self.random_background = random.choice(backgrounds)
        self.random_phrase = random.choice(list(Path(PHRASE_DIR).glob("*.*")))
        self.random_calendar = random.choice(
            list(Path(CALENDAR_DIR).glob(f"*{MONTHS[MONTH - 1]}*.*"))
        )

    def get_background(self):
        return self.random_background

    def get_phrase(self):
        return self.create_temp_image()

    def get_calendar(self):
        return self.random_calendar

    def get_position(self):
        return self.random_background.stem

    def get_random_quote(self):
        try:
            with open(QUOTES_FILE_DIR, "r") as file:
                line = next(file)
                for num, quote in enumerate(file, 2):
                    if random.randrange(num):
                        continue
                    line = quote
                return line.strip()
        except StopIteration:
            return None

    def create_temp_image(
        self, text_lines: List[str] = None, zodiac: str = None
    ) -> Image:
        text_color = (255, 255, 255)
        outline_color = (0, 0, 0)
        outline_width = 20
        if zodiac:
            zodiac = get_key_by_dict(ZODIAC_SINGS, zodiac)
            print(zodiac)
            zodiac_img = Image.open(f"{HOROSCOPE_IMG_DIR}{zodiac}.png").convert("RGBA")

            new_width = 130
            new_height = 100
            font_size = 35

            zodiac_img = zodiac_img.resize((new_width, new_height))

            width = 815
            height = 240
            new_img = Image.new("RGBA", (width, height))

            x_offset = (width - new_width) // 2
            y_offset = height // 2 - new_height
            new_img.paste(zodiac_img, (x_offset, y_offset))

            draw = ImageDraw.Draw(new_img)

            font = ImageFont.truetype(f"{FONTS_DIR}you20133.ttf", size=font_size)

            line_spacing = 5

            y_offset = 110
            for text in text_lines:
                text_width, text_height = draw.textsize(text, font=font)
                draw.text(
                    (width / 2 - 2, y_offset + text_height / 2),
                    text=text,
                    fill=(0, 0, 0),
                    font=font,
                    anchor="ma",
                )
                draw.text(
                    (width / 2, y_offset + text_height / 2),
                    text=text,
                    fill=text_color,
                    font=font,
                    anchor="ma",
                )
                y_offset += font_size + line_spacing

            return new_img
        font_size = 40
        line_spacing = 5
        text_lines = make_strings_from_text(self.get_random_quote())
        width = len(max(text_lines, key=len)) * 22
        height = len(text_lines) * (font_size + line_spacing * 2) + 16
        new_img = Image.new("RGBA", (width, height))
        font = ImageFont.truetype(f"{FONTS_DIR}you20133.ttf", size=font_size)
        y_offset = 0
        draw = ImageDraw.Draw(new_img)

        for text in text_lines:
            text_width, text_height = draw.textsize(text, font=font)
            draw.text(
                (width / 2 - 2, y_offset + text_height / 2),
                text=text,
                fill=(0, 0, 0),
                font=font,
                anchor="ma",
            )
            draw.text(
                (width / 2, y_offset + text_height / 2),
                text=text,
                fill=text_color,
                font=font,
                anchor="ma",
            )
            y_offset += font_size + line_spacing

        return new_img

    def make_wallpaper_v2(self, tg_id, input_zodiac=None):
        phrase_img = self.get_phrase()
        calendar_img = self.get_calendar()
        self.calendar.paste(self.get_background())
        position = self.get_position()
        coords = COORDS[position]

        if input_zodiac:
            zodiac = ZODIAC_SINGS[input_zodiac].lower()
            text_horo = get_text_from_json(zodiac)
            zodiac_img = self.create_temp_image(
                make_strings_from_text(text_horo), zodiac
            )

            width, height = phrase_img.size
            coords_center = ((940 - width) // 2, 400 - (height // 2))
            coords_right = ((950 - width) // 2, 540)
            coords_left = (((950 - width) // 2) + 950, 540)

            if position == "center":
                self.calendar.paste(phrase_img, coords_center, phrase_img)
                self.calendar.paste(calendar_img, coords["calendar"], calendar_img)
                self.calendar.paste(zodiac_img, coords["zodiac"], zodiac_img)
            elif position == "right":
                self.calendar.paste(phrase_img, coords_right, phrase_img)
                self.calendar.paste(
                    calendar_img, coords["calendar_with_horo"], calendar_img
                )
                self.calendar.paste(zodiac_img, coords["zodiac"], zodiac_img)
            else:
                self.calendar.paste(phrase_img, coords_left, phrase_img)
                self.calendar.paste(
                    calendar_img, coords["calendar_with_horo"], calendar_img
                )
                self.calendar.paste(zodiac_img, coords["zodiac"], zodiac_img)
        else:
            self.calendar.paste(phrase_img, coords["phrase"], phrase_img)
            self.calendar.paste(calendar_img, coords["calendar"], calendar_img)

        wallpaper_path = os.path.abspath(f"img/{tg_id}.png")
        self.calendar.save(wallpaper_path, quality=IMG_QUALITY)
        return wallpaper_path

    def make_wallpaper(self, tg_id, input_zodiac=None):
        phrase_img = self.get_phrase()
        calendar_img = self.get_calendar()
        self.calendar.paste(self.get_background())

        if input_zodiac:
            zodiac = ZODIAC_SINGS[input_zodiac].lower()
            zodiac_img = Image.open(f"{HOROSCOPE_IMG_DIR}{zodiac}.png")
            if "left" in self.random_background.name:
                self.calendar.paste(phrase_img, COORD_PHRASE_LEFT_WITH_HORO, phrase_img)
                self.calendar.paste(
                    calendar_img, COORD_CALENDAR_LEFT_WITH_HORO, calendar_img
                )
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_LEFT, zodiac_img)
            elif "right" in self.random_background.name:
                self.calendar.paste(
                    phrase_img, COORD_PHRASE_RIGHT_WITH_HORO, phrase_img
                )
                self.calendar.paste(
                    calendar_img, COORD_CALENDAR_RIGHT_WITH_HORO, calendar_img
                )
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_RIGHT, zodiac_img)
            else:
                self.calendar.paste(phrase_img, COORD_PHRASE_CENTER, phrase_img)
                self.calendar.paste(calendar_img, COORD_CALENDAR_CENTER, calendar_img)
                self.calendar.paste(zodiac_img, COORD_HOROSCOPE_CENTER, zodiac_img)
        else:
            if "left" in self.random_background.name:
                self.calendar.paste(phrase_img, COORD_PHRASE_LEFT, phrase_img)
                self.calendar.paste(calendar_img, COORD_CALENDAR_CENTER, calendar_img)
            elif "right" in self.random_background.name:
                self.calendar.paste(phrase_img, COORD_PHRASE_RIGHT, phrase_img)
                self.calendar.paste(calendar_img, COORD_CALENDAR_RIGHT, calendar_img)
            else:
                self.calendar.paste(phrase_img, COORD_PHRASE_CENTER, phrase_img)
                self.calendar.paste(calendar_img, COORD_CALENDAR_CENTER, calendar_img)

        wallpaper_path = os.path.abspath(f"img/{tg_id}.png")
        self.calendar.save(wallpaper_path, quality=IMG_QUALITY)
        return wallpaper_path


if __name__ == "__main__":
    a = CreateImage()
    # a.create_temp_image()
    # a.make_wallpaper_v2(1, "leo")
    text_list = [
        "Ох, уж, эти Водолеи. Весь месяц в кураже и",
        "внимании. Как же не упустить из виду нечто",
    ]
    a.create_temp_image(text_list, "aquarius")
