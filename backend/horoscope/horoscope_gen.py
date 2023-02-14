import asyncio
import json
from datetime import datetime
from pprint import pprint

from settings.config import MONTHLY_HOROSCOPE_DIR

NOW_MONTH = datetime.now().month


async def get_horoscope(sign):
    with open(f'{MONTHLY_HOROSCOPE_DIR}{NOW_MONTH}.json', 'r') as file:
        zodiac_info = json.load(file)

    if sign in zodiac_info:
        return dict(zodiac_info[sign])
    return "Знак не найден в базе."


async def main():
    sign = input("Ваш зодиак: ")
    result = await get_horoscope(sign)
    pprint(result.get('Любовь'))

if __name__ == '__main__':
    asyncio.run(main())
