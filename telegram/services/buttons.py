import config
from aiogram import types
from config import bot


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


async def create_welcome_message(message: types.Message,
                                 text_message=config.WELCOME_MESSAGE,
                                 zodiac=None):
    text = 'Знак зодиака' if not zodiac else 'Календарь с гороскопом'
    await bot.send_message(
        chat_id=message.chat.id,
        text=text_message,
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [types.KeyboardButton(text=text),
                 types.KeyboardButton(text="Создать календарь"), ],
                [types.KeyboardButton(
                    text="Получить гороскоп"), ] if zodiac else [
                    types.KeyboardButton(text="Подписка"), ],
                [types.KeyboardButton(
                    text="Подписка"), ] if zodiac else [
                    types.KeyboardButton(text="Назад"), ]
            ]
        )
    )


async def subscribe_menu(message: types.Message, sub_motivation_text,
                         sub_horoscope_text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(sub_motivation_text, sub_horoscope_text)
    markup.add('Назад')
    await bot.send_message(
        chat_id=message.chat.id,
        text='Вы подписчик! Теперь вы можете подписаться на ежедневные '
             'мотивации и гороскоп!',
        reply_markup=markup
    )
