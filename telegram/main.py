import asyncio
import datetime
import logging

import aioschedule
import config
from aiogram import executor, types
from aiohttp import ClientSession
from config import bot, dp
from services.buttons import (create_start_button, create_welcome_message,
                              subscribe_menu)
from services.other import get_all_subscriber, get_user_data

API_TOKEN = config.BOT_API_KEY
CREATE_USER_URL = config.API_DOMEN + config.USER_CREATE_API
GET_CALENDAR_URL = config.API_DOMEN + config.CREATE_CALENDAR_API
GET_MONTHLY_HOROSCOPE = config.API_DOMEN + config.MONTHLY_HOROSCOPE_API

ZODIAC_SINGS = [
    'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион',
    'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    username = (message.from_user.username if message.from_user.username
                else message.from_user.first_name)

    data = {
        "tg_id": tg_id,
        "username": username
    }

    async with ClientSession() as session:
        async with session.post(CREATE_USER_URL, json=data) as response:
            if response.status == 200:
                logging.info(f'Add user {username}')
            else:
                logging.error(f'Failed to add user {username}')
            user_data = await response.json()
        await create_welcome_message(message, zodiac=user_data.get('zodiac'))


@dp.message_handler(lambda message: message.text == 'Знак зодиака')
async def get_zodiac_buttons(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for sign in ZODIAC_SINGS:
        markup.add(types.KeyboardButton(sign))

    await bot.send_message(
        chat_id=message.chat.id,
        text='Пожалуйста, выберите знак зодиака:',
        reply_markup=markup
    )


@dp.message_handler(lambda message: message.text in ZODIAC_SINGS)
async def add_user_zodiac(message: types.Message):
    tg_id = message.from_user.id
    sign = message.text
    username = message.from_user.username
    add_zodiac_url = CREATE_USER_URL + f'{tg_id}/zodiac/'

    data = {
        "zodiac": sign
    }

    async with ClientSession() as session:
        async with session.put(add_zodiac_url, json=data) as response:
            if response.status == 200:
                logging.info(
                    f'Пользователю {username} добавлен знак зодиака {sign}'
                )
            else:
                logging.error(f'Ошибка добавления зодиака {username}')

    await create_welcome_message(message,
                                 'Теперь ты можешь можешь получить гороскоп!',
                                 data.get('zodiac'))


@dp.message_handler(lambda message: message.text == 'Календарь с гороскопом')
async def create_calendar(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    async with ClientSession() as session:
        data = await get_user_data(message, session)
        async with session.post(
                GET_CALENDAR_URL + f'?tg_id={tg_id}',
                json={'zodiac': data.get('zodiac')}) as response:
            if response.status == 200:
                logging.info(
                    f'Календарь для пользователя {username} создан'
                )
                file = await response.read()
                await bot.send_photo(chat_id=message.chat.id, photo=file)
            else:
                logging.error(f'Ошибка создания календаря для {username}')


@dp.message_handler(lambda message: message.text == 'Создать календарь')
async def create_calendar(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    async with ClientSession() as session:
        async with session.post(
                GET_CALENDAR_URL + f'?tg_id={tg_id}') as response:
            if response.status == 200:
                logging.info(
                    f'Календарь для пользователя {username} создан'
                )
                file = await response.read()
                await bot.send_photo(chat_id=message.chat.id, photo=file)
            else:
                logging.error(f'Ошибка создания календаря для {username}')


@dp.message_handler(lambda message: message.text == 'Получить гороскоп')
async def get_monthly_horoscope(message: types.Message):
    tg_id = message.from_user.id

    async with ClientSession() as session:
        async with session.post(
                GET_MONTHLY_HOROSCOPE + f'?tg_id={tg_id}') as response:
            if response.status == 200:
                data = await response.json()
                if data.get('detail') == 'Пользователя нет в базе':
                    await create_start_button(message)
                elif data.get('detail') == 'Не заполнен знак зодиака':
                    await get_zodiac_buttons(message)
                else:
                    for cat in data:
                        await bot.send_message(
                            chat_id=message.chat.id,
                            text=f'{cat}\n{data.get(cat)}'
                        )


@dp.message_handler(lambda message: message.text == 'Подписка')
async def subscribe(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    name = username if username else message.from_user.first_name
    subscribe_url = f'{CREATE_USER_URL}{tg_id}/{config.SUBSCRIBE_API}'

    async with ClientSession() as session:
        async with session.put(subscribe_url) as response:
            if response.status == 200:
                logging.info(f'Пользователь {name} подписался')
            else:
                logging.error(f'Ошибка подписки пользователя {name}')
        data = await get_user_data(message, session)

    if data.get('is_subscriber'):
        sub_motivation_text = 'Отписаться от мотивации' if data.get(
            'is_quote_subscribe') else 'Подписаться на мотивацию'
        sub_horoscope_text = 'Отписаться от гороскопа' if data.get(
            'is_horoscope_subscribe') else 'Подписаться на гороскоп'

    await subscribe_menu(message, sub_motivation_text, sub_horoscope_text)


@dp.message_handler(lambda message: message.text == 'Назад')
async def back(message: types.Message):
    async with ClientSession() as session:
        data = await get_user_data(message, session)
    if data.get('detail') == 'Пользователь не найден':
        await create_start_button(message)
    else:
        await create_welcome_message(message, 'Что сделаем?',
                                     data.get('zodiac'))


@dp.message_handler(lambda message: message.text == 'Подписаться на мотивацию')
async def subscribe_to_quotes(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    subscribe_quotes_url = (
        f'{config.API_DOMEN}{config.SUBSCRIBE_QUOTES_API}?tg_id={tg_id}'
    )
    async with ClientSession() as session:
        async with session.put(subscribe_quotes_url) as response:
            if response.status == 200:
                logging.info(
                    f'Пользователь {username} подписался на ежедневную '
                    f'мотивацию.')
                await send_daily_motivation(bot, tg_id)
            else:
                logging.error(f'Ошибка подписки пользователя {username}')


# @dp.message_handler(
# lambda message: message.text == 'Подписаться на гороскоп')
async def send_daily_motivation(bot, tg_id):
    get_motivation_url = (
        f'{config.API_DOMEN}{config.GET_DAILY_QUOTES_API}{tg_id}'
    )
    async with ClientSession() as session:
        async with session.post(get_motivation_url) as response:
            if response.status == 200:
                data = await response.json()
                quote = data.get('quote')
                logging.info('Ежедневная мотивация получена')
            else:
                logging.error('Ошибка получения мотивации')

    await bot.send_message(chat_id=tg_id,
                           text=f'Мотивация на сегодня:\n{quote}')


async def scheduled():
    while True:
        now = datetime.datetime.now()
        logging.info('Начинаю отправку сообщений подписчикам')
        async with ClientSession() as session:
            data = await get_all_subscriber(session)
            motivation_subscribes = data.get('quote_subscribers')

        if now.hour == 6:
            for user in motivation_subscribes:
                await send_daily_motivation(bot, user)

        await aioschedule.run_pending()
        await asyncio.sleep(3600)


async def on_startup(dp):
    asyncio.create_task(scheduled())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
