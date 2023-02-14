import random

from settings.config import QUOTES_FILE_DIR


async def get_random_quote():
    try:
        with open(QUOTES_FILE_DIR, 'r') as file:
            line = next(file)
            for num, quote in enumerate(file, 2):
                if random.randrange(num):
                    continue
                line = quote
            return line.strip()
    except StopIteration:
        return None


async def main():
    await get_random_quote()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
