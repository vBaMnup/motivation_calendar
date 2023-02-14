from typing import Any

from aiogram.types import Message
from config import API_DOMEN, GET_ALL_SUBSCRIBER_API, USER_CREATE_API


async def get_user_data(message: Message, session) -> Any:
    tg_id: int = message.from_user.id
    user_data_url: str = f'{API_DOMEN}{USER_CREATE_API}{tg_id}/'

    async with session.get(user_data_url) as response:
        return await response.json()


async def get_all_subscriber(session) -> Any:
    all_subscriber_url = f'{API_DOMEN}{GET_ALL_SUBSCRIBER_API}'

    async with session.get(all_subscriber_url) as response:
        return await response.json()
