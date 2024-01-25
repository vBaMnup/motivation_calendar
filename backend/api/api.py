from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from daily_motivation.motivation_quote_creater import get_random_quote
from horoscope.horoscope_gen import get_horoscope, get_today_horoscope
from pictures.pic_maker import CreateImage
from .models import users
from .schema import User, Zodiac

img_router = APIRouter()


@img_router.post("/users/")
async def create_user(user: User):
    """
    Создание нового пользователя
    """
    temp_user = users.find_one({"tg_id": user.tg_id}, {"_id": 0})
    if temp_user:
        return temp_user
    user_data = {
        "tg_id": user.tg_id,
        "username": user.username,
        "zodiac": user.zodiac,
        "count_request_calendar": 0,
        "count_request_horoscope": 0,
        "is_subscriber": False,
        "is_quote_subscribe": False,
        "is_horoscope_subscribe": False,
    }
    users.insert_one(user_data)
    return user


@img_router.put("/users/{tg_id}/zodiac")
async def update_user_zodiac(tg_id: int, zodiac: Zodiac):
    result = users.update_one({"tg_id": tg_id}, {"$set": {"zodiac": zodiac.zodiac}})
    return (
        {"result": "Zodiac updated"}
        if result.modified_count
        else {"result": "User not found"}
    )


@img_router.put("/users/{tg_id}/is_subscriber")
async def update_user_is_subscriber(tg_id: int, is_subscriber: bool):
    """
    Обновление статуса подписки пользователя
    """
    result = users.update_one(
        {"tg_id": tg_id}, {"$set": {"is_subscriber": is_subscriber}}
    )
    return (
        {"result": "Is subscriber request updated"}
        if result.modified_count
        else {"result": "User not found"}
    )


@img_router.put("/subscribe_to_quotes")
async def subscribe_to_quotes(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if not user_data:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_subscriber"):
        raise HTTPException(
            status_code=400,
            detail="Невозможно подписаться на ежедневную мотивацию, "
            "т.к. пользователь не является подписчиком",
        )
    users.update_one({"tg_id": tg_id}, {"$set": {"is_quote_subscribe": True}})
    return {"message": "Подписка на ежедневную мотивацию успешно оформлена"}


@img_router.put("/unsubscribe_from_quotes")
async def unsubscribe_from_quotes(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if not user_data:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_quote_subscribe"):
        raise HTTPException(
            status_code=400, detail="Пользователь не подписан на ежедневную мотивацию"
        )
    users.update_one({"tg_id": tg_id}, {"$set": {"is_quote_subscribe": False}})
    return {"message": "Отписка от ежедневной мотивации успешно выполнена"}


@img_router.put("/subscribe_to_horoscope")
async def subscribe_to_horoscope(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if not user_data:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_subscriber"):
        raise HTTPException(
            status_code=400,
            detail="Невозможно подписаться на ежедневный гороскоп, "
            "т.к. пользователь не является подписчиком",
        )
    users.update_one({"tg_id": tg_id}, {"$set": {"is_horoscope_subscribe": True}})
    return {"message": "Подписка на ежедневный гороскоп успешно оформлена"}


@img_router.put("/unsubscribe_from_horoscope")
async def unsubscribe_from_horoscope(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if not user_data:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_horoscope_subscribe"):
        raise HTTPException(
            status_code=400, detail="Пользователь не подписан на ежедневный гороскоп"
        )
    users.update_one({"tg_id": tg_id}, {"$set": {"is_horoscope_subscribe": False}})
    return {"message": "Отписка от ежедневного гороскопа успешно выполнена"}


@img_router.get("/users/")
async def get_all_users():
    """
    Получение всех зарегистрированных пользователей
    """
    all_users = list(users.find({}, {"_id": 0}))
    return 1  # {"users": all_users}


@img_router.get("/get_all_subscriber")
async def get_all_subscriber():
    quote_subscribers = list(
        user.get("tg_id")
        for user in users.find(
            {"is_subscriber": True, "is_quote_subscribe": True}, {"_id": 0}
        )
    )
    horoscope_subscribers = list(
        user.get("tg_id")
        for user in users.find(
            {"is_subscriber": True, "is_horoscope_subscribe": True}, {"_id": 0}
        )
    )
    return {
        "quote_subscribers": quote_subscribers,
        "horoscope_subscribers": horoscope_subscribers,
    }


@img_router.get("/users/{tg_id}")
async def get_user(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id}, {"_id": 0})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    return user_data


@img_router.delete("/delete_user")
async def delete_user(tg_id: int):
    user_data = users.find_one(({"tg_id": tg_id}))
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    users.delete_one({"tg_id": tg_id})
    return {"result": "Пользователь удален"}


@img_router.post("/get_calendar")
async def get_calendar(tg_id: int, zodiac: Zodiac = None):
    user_data = users.find_one({"tg_id": tg_id})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    """ Пока неактивно
    if (user_data.get('count_request') > 0
            and not user_data.get('is_subscriber')):
        raise HTTPException(
            status_code=400,
            detail='Пользователь без активной подписки может делать только 1 '
                   'запрос в месяц'
        )
    """

    users.update_one({"tg_id": tg_id}, {"$inc": {"count_request_calendar": 1}})

    if zodiac:
        return FileResponse(
            CreateImage().make_wallpaper_v2(tg_id, user_data.get("zodiac")),
            media_type="image/jpeg",
        )
    return FileResponse(CreateImage().make_wallpaper_v2(tg_id), media_type="image/jpeg")


@img_router.post("/monthly_horoscope/")
async def get_monthly_horoscope(tg_id: int):
    try:
        user_zodiac = users.find_one(({"tg_id": tg_id})).get("zodiac")
    except AttributeError:
        return HTTPException(status_code=400, detail="Пользователя нет в базе")

    if user_zodiac is None:
        return HTTPException(status_code=400, detail="Не заполнен знак зодиака")

    users.update_one({"tg_id": tg_id}, {"$inc": {"count_request_horoscope": 1}})
    return await get_horoscope(user_zodiac)


@img_router.post("/get_daily_motivation")
async def get_daily_motivation(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if not user_data:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_subscriber") or not user_data.get("is_quote_subscribe"):
        raise HTTPException(
            status_code=400,
            detail="Только подписчики с активной подпиской на цитаты могут "
            "получать ежедневную мотивацию",
        )
    return {"quote": await get_random_quote()}


@img_router.post("/get_daily_horoscope")
async def get_daily_horoscope(tg_id: int):
    user_data = users.find_one({"tg_id": tg_id})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not user_data.get("is_subscriber") or not user_data.get(
        "is_horoscope_subscribe"
    ):
        raise HTTPException(
            status_code=400,
            detail="Только подписчики с активной подпиской на гороскоп могут "
            "получать ежедневную мотивацию",
        )
    zodiac = user_data.get("zodiac")
    if not zodiac:
        raise HTTPException(status_code=400, detail="Укажите знак зодиака")
    return {"horoscope": await get_today_horoscope(zodiac)}
