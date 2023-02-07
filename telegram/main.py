import logging

from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession

import config

API_TOKEN = config.BOT_API_KEY
CREATE_USER_URL = config.API_DOMEN + config.USER_CREATE_API
GET_CALENDAR_URL = config.API_DOMEN + config.CREATE_CALENDAR_API
GET_MONTHLY_HOROSCOPE = config.API_DOMEN + config.MONTHLY_HOROSCOPE_API

ZODIAC_SINGS = [
    'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион',
    'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


async def create_start_button(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Привет, нажми кнопку start, чтобы начать :)",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text="/start")]
            ]
        )
    )


async def create_welcome_message(message: types.Message, zodiac=None):
    text = 'Знак зодиака' if not zodiac else 'Календарь с гороскопом'
    await bot.send_message(
        chat_id=message.chat.id,
        text="Привет, нажми на создать календарь или добавь знак зодиака,"
             " чтобы получить гороскоп на месяц.",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text=text),
                 types.KeyboardButton(text="Создать календарь"), ],
                [types.KeyboardButton(
                    text="Получить гороскоп"), ] if zodiac else [
                    types.KeyboardButton(text="/start"), ]
            ]
        )
    )


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
        await create_welcome_message(message, user_data.get('zodiac'))
    # if not user_data.get('zodiac'):
    #     await bot.send_message(
    #         chat_id=message.chat.id,
    #         text="Привет, нажми на создать календарь или добавь знак
    #         зодиака,"
    #              " чтобы получить гороскоп на месяц.",
    #         reply_markup=types.ReplyKeyboardMarkup(
    #             resize_keyboard=True, keyboard=[
    #                 [types.KeyboardButton(
    #                     text="Знак зодиака" if not user_data.get(
    #                         'zodiac') else "Получить гороскоп"
    #                 ),
    #                     types.KeyboardButton(text="Создать календарь"), ]
    #             ]
    #         )
    #     )


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

    await bot.send_message(
        chat_id=message.chat.id,
        text="Теперь ты можешь можешь получить гороскоп!",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text="Создать календарь"),
                 types.KeyboardButton(text="Календарь с гороскопом"), ],
                [types.KeyboardButton(text="Получить гороскоп"), ]
            ]
        )
    )


@dp.message_handler(lambda message: message.text == 'Календарь с гороскопом')
async def create_calendar(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    async with ClientSession() as session:
        async with session.get(CREATE_USER_URL + f'{tg_id}/') as response:
            data = await response.json()
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
