import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from PIL import Image, ImageDraw, ImageFont

# Импорт вспомогательных функций и настроек
from pictures.string_split import (
    get_text_from_json,
    make_strings_from_text,
)
from settings.config import (
    BACKGROUNDS_DIR,
    CALENDAR_DIR,
    COORD_MAP,
    HOROSCOPE_IMG_DIR,
    IMG_RESOLUTION,
    PHRASE_DIR,
    WINTER,
    ZODIAC_SIGNS,
    FONTS_DIR,
    TEXT_SHADOW_OFFSET,
    FONT_SIZE_REGULAR,
    FONT_SIZE_SMALL,
    LINE_SPACING,
)

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


class ImageCache:
    """Класс для кэширования путей к файлам изображений"""

    _instance = None
    _backgrounds: Dict[str, List[Path]] = {}
    _phrases: List[Path] = []
    _calendars: Dict[str, List[Path]] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def initialize(cls):
        cls._phrases = list(Path(PHRASE_DIR).glob("*.*"))
        await cls._load_backgrounds()
        await cls._load_calendars()

    @classmethod
    async def _load_backgrounds(cls):
        for month in range(1, 13):
            key = "winter" if month in WINTER else "default"
            if key not in cls._backgrounds:
                path = Path(BACKGROUNDS_DIR) / ("winter" if key == "winter" else "")
                cls._backgrounds[key] = list(path.glob("*.*"))

    @classmethod
    async def _load_calendars(cls):
        for month in range(1, 13):
            month_name = MONTHS[month - 1]
            if month_name not in cls._calendars:
                cls._calendars[month_name] = list(
                    Path(CALENDAR_DIR).glob(f"*{month_name}*.*")
                )

    @classmethod
    def get_backgrounds(cls, month: int) -> List[Path]:
        key = "winter" if month in WINTER else "default"
        return cls._backgrounds.get(key, [])

    @classmethod
    def get_phrases(cls) -> List[Path]:
        return cls._phrases

    @classmethod
    def get_calendars(cls, month: int) -> List[Path]:
        return cls._calendars.get(MONTHS[month - 1], [])


class AsyncImageProcessor:
    """Обработчик изображений с асинхронным API"""

    _executor = ThreadPoolExecutor()
    _font_cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}

    @classmethod
    async def open_image(cls, path: Path) -> Image.Image:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(cls._executor, Image.open, path)

    @classmethod
    async def load_font(cls, font_path: str, size: int) -> ImageFont.FreeTypeFont:
        key = (font_path, size)
        if key not in cls._font_cache:
            loop = asyncio.get_event_loop()
            font = await loop.run_in_executor(
                cls._executor, ImageFont.truetype, font_path, size
            )
            cls._font_cache[key] = font
        return cls._font_cache[key]

    @classmethod
    async def draw_text_with_shadow(
        cls,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        color: Tuple[int, int, int] = (255, 255, 255),
        shadow_color: Tuple[int, int, int] = (0, 0, 0),
        anchor: str = "ma",
    ) -> None:
        x, y = position
        draw.text(
            (x - TEXT_SHADOW_OFFSET, y), text, shadow_color, font=font, anchor=anchor
        )
        draw.text((x, y), text, color, font=font, anchor=anchor)


class WallpaperCreator:
    """Основной класс для создания обоев"""

    def __init__(self):
        self.month = datetime.today().month
        self._init_paths()
        self.calendar_image = Image.new("RGB", IMG_RESOLUTION)

    def _init_paths(self):
        self.background_path = random.choice(ImageCache.get_backgrounds(self.month))
        self.phrase_path = random.choice(ImageCache.get_phrases())
        self.calendar_path = random.choice(ImageCache.get_calendars(self.month))

    @property
    def position(self) -> str:
        name = self.background_path.name.lower()
        return next((p for p in ["left", "right", "center"] if p in name), "center")

    async def _create_zodiac_image(
        self, text_lines: List[str], zodiac: str
    ) -> Image.Image:
        # zodiac_key = ZODIAC_SIGNS.get(zodiac.lower())
        zodiac_img = await AsyncImageProcessor.open_image(
            Path(HOROSCOPE_IMG_DIR) / f"{zodiac}.png"
        )
        zodiac_img = zodiac_img.resize((130, 100)).convert("RGBA")

        base_image = Image.new("RGBA", (815, 240))
        base_image.paste(zodiac_img, ((815 - 130) // 2, 20))

        draw = ImageDraw.Draw(base_image)
        font = await AsyncImageProcessor.load_font(
            str(Path(FONTS_DIR) / "you20133.ttf"), FONT_SIZE_SMALL
        )

        y_offset = 110
        for text in text_lines:
            await AsyncImageProcessor.draw_text_with_shadow(
                draw, (407, y_offset), text, font
            )
            y_offset += FONT_SIZE_SMALL + LINE_SPACING

        return base_image

    async def _create_quote_image(self, text_lines: List[str]) -> Image.Image:
        max_line_length = max(len(line) for line in text_lines) if text_lines else 0
        width = max_line_length * 22
        height = len(text_lines) * (FONT_SIZE_REGULAR + LINE_SPACING) + 16

        base_image = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(base_image)
        font = await AsyncImageProcessor.load_font(
            str(Path(FONTS_DIR) / "you20133.ttf"), FONT_SIZE_REGULAR
        )

        y_offset = 0
        for text in text_lines:
            await AsyncImageProcessor.draw_text_with_shadow(
                draw, (width // 2, y_offset + FONT_SIZE_REGULAR // 2), text, font
            )
            y_offset += FONT_SIZE_REGULAR + LINE_SPACING

        return base_image

    async def create_text_image(
        self, text_lines: Optional[List[str]] = None, zodiac: Optional[str] = None
    ) -> Image.Image:
        if zodiac:
            return await self._create_zodiac_image(text_lines or [], zodiac)
        return await self._create_quote_image(text_lines or [])

    async def generate_wallpaper(
        self, user_id: int, zodiac: Optional[str] = None
    ) -> Path:
        background, phrase_img, calendar_img = await asyncio.gather(
            AsyncImageProcessor.open_image(self.background_path),
            AsyncImageProcessor.open_image(self.phrase_path),
            AsyncImageProcessor.open_image(self.calendar_path),
        )

        self.calendar_image.paste(background)
        coords = COORD_MAP[self.position]

        if zodiac:
            text = get_text_from_json(ZODIAC_SIGNS[zodiac].lower())
            horo_img = await self.create_text_image(
                make_strings_from_text(text), zodiac
            )
            components = [
                (phrase_img, coords["phrase"]),
                (calendar_img, coords["calendar"]),
                (horo_img, coords["zodiac"]),
            ]
        else:
            components = [
                (phrase_img, coords["phrase"]),
                (calendar_img, coords["calendar"]),
            ]

        for img, coord in components:
            self.calendar_image.paste(img, coord, img)

        output_path = Path("img") / f"{user_id}.png"
        await asyncio.get_event_loop().run_in_executor(
            AsyncImageProcessor._executor,
            self.calendar_image.save,
            output_path,
            # quality=IMG_QUALITY
        )
        return output_path


async def main():
    await ImageCache.initialize()
    tasks = [WallpaperCreator().generate_wallpaper(i, "leo") for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"Generated wallpapers: {[str(p) for p in results]}")


if __name__ == "__main__":
    asyncio.run(main())

    # a = CreateImage()
    # # a.create_temp_image()
    # a.make_wallpaper_v2(0, "leo")
    # text_list = [
    #     "Ох, уж, эти Водолеи. Весь месяц в кураже и",
    #     "внимании. Как же не упустить из виду нечто",
    # ]
    # a.create_temp_image(text_list, "aquarius")
