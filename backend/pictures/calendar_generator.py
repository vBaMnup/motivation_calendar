import asyncio
import calendar
from pathlib import Path
from typing import Tuple, Optional
from functools import partial
from PIL import Image, ImageDraw, ImageFont


class CalendarGenerator:
    """Класс генератора календарей с асинхронным API"""

    DEFAULT_FONT = ImageFont.load_default()
    TEXT_SHADOW_OFFSET = 1
    MIN_CONTRAST_RATIO = 128

    def __init__(self, background_path: Path):
        """Инициализация генератора календарей"""
        self.background_path = background_path
        self.output_path: Optional[Path] = None
        self._bg_image: Optional[Image.Image] = None

    async def load_background(self) -> None:
        """
        Асинхронная загрузка фонового изображения

        Raises:
            RuntimeError: Если не удалось загрузить фоновое изображение
        """
        loop = asyncio.get_event_loop()
        try:
            self._bg_image = await loop.run_in_executor(
                None, partial(Image.open, self.background_path)
            )
        except (IOError, OSError) as e:
            raise RuntimeError(f"Error loading background image: {e}") from e

    def _calculate_text_color(self) -> Tuple[int, int, int, int]:
        """
        Вычисление оптимального цвета текста на основе яркости фона

        Returns:
            Tuple[int, int, int, int]: Кортеж с цветом текста
        """
        if self._bg_image is None:
            return (255, 255, 255, 255)

        gray_image = self._bg_image.convert("L")
        brightness = gray_image.resize((1, 1)).getpixel((0, 0))
        color = (0, 0, 0) if brightness > self.MIN_CONTRAST_RATIO else (255, 255, 255)
        return (*color, 255)

    def _generate_calendar_overlay(
        self,
        year: int,
        month: int,
        size: Tuple[int, int],
        font: ImageFont.FreeTypeFont = DEFAULT_FONT,
    ) -> Image.Image:
        """
        Генерация прозрачного overlay с календарём

        Args:
            year (int): Год
            month (int): Месяц
            size (Tuple[int, int]): Размер overlay
            font (ImageFont.FreeTypeFont, optional): Шрифт. По умолчанию используется DEFAULT_FONT

        Returns:
            Image.Image: Overlay с календарём
        """
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")

        cal_text = calendar.month(year, month)
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Использование textbbox вместо устаревшего textsize
        bbox = draw.textbbox((0, 0), cal_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

        draw.text(position, cal_text, font=font, fill=self._calculate_text_color())
        return overlay

    async def generate(
        self,
        year: int,
        month: int,
        output_path: Path,
        calendar_size: Tuple[int, int],
        position: Tuple[int, int],
        font_path: Optional[Path] = None,
    ) -> None:
        """
        Основной метод генерации календаря

        Args:
            year (int): Год
            month (int): Месяц
            output_path (Path): Путь для сохранения результата
            calendar_size (Tuple[int, int]): Размер overlay
            position (Tuple[int, int]): Позиция overlay
            font_path (Optional[Path], optional): Путь к кастомному шрифту
        """
        await self.load_background()

        font = self.DEFAULT_FONT
        if font_path and font_path.exists():
            font = await self._load_custom_font(font_path)

        overlay = await asyncio.get_event_loop().run_in_executor(
            None,
            partial(self._generate_calendar_overlay, year, month, calendar_size, font),
        )

        await self._apply_overlay(overlay, position)
        await self._save_image(output_path)

    async def _load_custom_font(self, font_path: Path) -> ImageFont.FreeTypeFont:
        """
        Асинхронная загрузка кастомного шрифта

        Args:
            font_path (Path): Путь к кастомному шрифту

        Returns:
            ImageFont.FreeTypeFont: Шрифт
        """
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(None, ImageFont.truetype, str(font_path))
        except IOError as e:
            print(f"Error loading font: {e}. Using default font.")
            return self.DEFAULT_FONT

    async def _apply_overlay(
        self, overlay: Image.Image, position: Tuple[int, int]
    ) -> None:
        """
        Применение overlay к фоновому изображению

        Args:
            overlay (Image.Image): Overlay с календарём
            position (Tuple[int, int]): Позиция overlay
        """
        if self._bg_image is None:
            raise RuntimeError("Background image not loaded")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, partial(self._bg_image.paste, overlay, position, overlay)
        )

    async def _save_image(self, output_path: Path) -> None:
        """
        Асинхронное сохранение результата

        Args:
            output_path (Path): Путь для сохранения результата
        """
        if self._bg_image is None:
            raise RuntimeError("No image to save")

        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, partial(self._bg_image.save, output_path))
        except (IOError, OSError) as e:
            raise RuntimeError(f"Error saving image: {e}") from e


async def main():
    try:
        config = {
            "background_path": Path("background.jpg"),
            "output_path": Path("calendar_output.png"),
            "year": 2025,
            "month": 2,
            "calendar_size": (1000, 1000),
            "position": (50, 50),
            "font_path": Path("arial.ttf"),
        }

        generator = CalendarGenerator(config["background_path"])
        await generator.generate(
            year=config["year"],
            month=config["month"],
            output_path=config["output_path"],
            calendar_size=config["calendar_size"],
            position=config["position"],
            font_path=config["font_path"],
        )
        print("Calendar successfully generated")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
