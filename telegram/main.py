import logging
from pprint import pprint
from aiohttp import ClientSession

import requests
from aiogram import Bot, Dispatcher, executor, types

import config

API_TOKEN = config.BOT_API_KEY
CREATE_USER_URL = config.API_DOMEN + config.USER_CREATE_API
GET_CALENDAR_URL = config.API_DOMEN + config.CREATE_CALENDAR_API

ZODIAC_SINGS = [
        'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион',
        'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
    ]
CREATE_CALENDAR_COMMANDS = ['Создать календарь', 'Календарь с гороскопом']

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.first_name

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

    await bot.send_message(
        chat_id=message.chat.id,
        text="Привет, нажми на создать календарь или добавь знак зодиака,"
             " если хочешь, чтобы на календаре был гороскоп на месяц",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text="Знак зодиака"),
                 types.KeyboardButton(text="Создать календарь"), ]
            ]
        )
    )


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
    print(add_zodiac_url)

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

    await bot.send_message(
        chat_id=message.chat.id,
        text="Теперь ты можешь создать календарь со своим гороскопом",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text="Создать календарь"),
                 types.KeyboardButton(text="Календарь с гороскопом"), ]
            ]
        )
    )


@dp.message_handler(lambda message: message.text in CREATE_CALENDAR_COMMANDS)
async def create_calendar(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    async with ClientSession() as session:
        async with session.post(GET_CALENDAR_URL + f'?tg_id={tg_id}') as response:
            if response.status == 200:
                logging.info(
                    f'Календарь для пользователя {username} создан'
                )
                file = await response.read()
                await bot.send_photo(chat_id=message.chat.id, photo=file)
            else:
                logging.error(f'Ошибка создания календаря для {username}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
