import config
from aiogram import types
from config import ZODIAC_SINGS, bot


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


async def create_zodiac_buttons(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for en_sign in ZODIAC_SINGS.keys():
        markup.add(types.KeyboardButton(en_sign))

    await bot.send_message(
        chat_id=message.chat.id,
        text='Пожалуйста, выберите знак зодиака:',
        reply_markup=markup
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


async def subscribe_menu(message: types.Message, sub_motivation_data,
                         sub_horoscope_data, text=config.SUBSCRIBER_TEXT):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    sub_quote_text = {
        False: 'Подписаться на мотивацию',
        True: 'Отписаться от мотивации'
    }
    sub_horo_text = {
        False: 'Подписаться на гороскоп',
        True: 'Отписаться от гороскопа'
    }
    markup.add(sub_quote_text[sub_motivation_data],
               sub_horo_text[sub_horoscope_data])
    markup.add('Назад')
    await bot.send_message(chat_id=message.chat.id, text=text,
                           reply_markup=markup)
