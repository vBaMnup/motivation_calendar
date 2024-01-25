import random

import aiofiles

from settings.config import QUOTES_FILE_DIR


async def get_random_quote():
    try:
        async with aiofiles.open(QUOTES_FILE_DIR, "r") as file:
            lines = await file.readlines()
            return random.choice(lines).strip()
    except (FileNotFoundError, IndexError):
        return None


async def main():
    quote = await get_random_quote()
    print(quote)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
