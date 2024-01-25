import json
import os
from datetime import datetime
from xml.etree import ElementTree

import aiofiles
from aiohttp import ClientSession

from settings.config import DAILY_HOROSCOPE_DIR, MONTHLY_HOROSCOPE_DIR, ZODIAC_SINGS

NOW_MONTH = datetime.now().month


async def get_horoscope(sign: str) -> dict | str:
    async with aiofiles.open(f"{MONTHLY_HOROSCOPE_DIR}{NOW_MONTH}.json", "r") as file:
        zodiac_info = json.load(await file.read())

    ru_sign = ZODIAC_SINGS.get(sign)

    if ru_sign in zodiac_info:
        return dict(zodiac_info[ru_sign])
    return "Знак не найден в базе."


async def get_today_horoscope(sign: str) -> str:
    cache_file_name = f"{DAILY_HOROSCOPE_DIR}horoscope_{datetime.today().day}.xml"
    horoscope_url = "https://ignio.com/r/export/utf/xml/daily/com.xml"
    if not os.path.exists(cache_file_name):
        async with ClientSession() as session:
            async with session.get(horoscope_url) as response:
                xml = await response.text()

        async with aiofiles.open(cache_file_name, "w") as cache_file:
            await cache_file.write(xml)
    else:
        async with aiofiles.open(cache_file_name, "r") as cache_file:
            xml = await cache_file.read()

    root = ElementTree.fromstring(xml)
    horoscope = root.find(sign)
    if not horoscope:
        return f"Гороскоп для {sign} не найден"
    return horoscope.find("today").text.strip()


async def main():
    # sign = input("Ваш зодиак: ")
    # result = await get_horoscope(sign)
    # pprint(result.get('Любовь'))
    result = await get_today_horoscope("scorpio")
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
