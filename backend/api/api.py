from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from pictures.pic_maker import CreateImage
from .models import users
from .schema import User, Zodiac
from horoscope.horoscope_gen import get_horoscope

img_router = APIRouter()


@img_router.post("/users/")
async def create_user(user: User):
    """
    Создание нового пользователя
    """
    temp_user = users.find_one({'tg_id': user.tg_id}, {"_id": 0})
    if temp_user:
        return temp_user
    user_data = {
        "tg_id": user.tg_id,
        "username": user.username,
        "zodiac": user.zodiac,
        "count_request": 0,
        "is_subscriber": False
    }
    users.insert_one(user_data)
    return user


@img_router.put("/users/{tg_id}/zodiac")
async def update_user_zodiac(tg_id: int, zodiac: Zodiac):
    result = users.update_one(
        {"tg_id": tg_id}, {"$set": {"zodiac": zodiac.zodiac}}
    )
    return ({"result": "Zodiac updated"} if result.modified_count
            else {"result": "User not found"})


@img_router.put("/users/{tg_id}/is_subscriber")
async def update_user_is_subscriber(tg_id: int, is_subscriber: bool):
    """
    Обновление статуса подписки пользователя
    """
    result = users.update_one({"tg_id": tg_id}, {"$set": {
        "is_subscriber": is_subscriber
    }})
    return ({"result": "Is subscriber request updated"}
            if result.modified_count else {"result": "User not found"})


@img_router.get("/users/")
async def get_all_users():
    """
    Получение всех зарегистрированных пользователей
    """
    all_users = list(users.find({}, {"_id": 0}))
    return {"users": all_users}


@img_router.get("/users/{tg_id}")
async def get_user(tg_id: int):
    user_data = users.find_one({'tg_id': tg_id}, {"_id": 0})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    return user_data


@img_router.delete("/delete_user")
async def delete_user(tg_id: int):
    user_data = users.find_one(({'tg_id': tg_id}))
    if user_data is None:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не найден"
        )
    users.delete_one({'tg_id': tg_id})
    return {'result': 'Пользователь удален'}


@img_router.post("/get_calendar")
async def get_calendar(tg_id: int, zodiac: Zodiac = None):
    user_data = users.find_one({'tg_id': tg_id})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    ''' Пока неактивно
    if (user_data.get('count_request') > 0
            and not user_data.get('is_subscriber')):
        raise HTTPException(
            status_code=400,
            detail='Пользователь без активной подписки может делать только 1 '
                   'запрос в месяц'
        )
    '''

    users.update_one({'tg_id': tg_id}, {'$inc': {'count_request': 1}})

    if zodiac:
        return FileResponse(CreateImage().make_wallpaper(
                tg_id,
                user_data.get('zodiac')
            ), media_type='image/jpeg')
    return FileResponse(CreateImage().make_wallpaper(
        tg_id
    ), media_type='image/jpeg')


@img_router.post("/monthly_horoscope/")
async def get_monthly_horoscope(tg_id: int):
    try:
        user_zodiac = users.find_one(({'tg_id': tg_id})).get('zodiac')
    except AttributeError:
        return HTTPException(
            status_code=400, detail="Пользователя нет в базе"
        )

    if user_zodiac is None:
        return HTTPException(
            status_code=400, detail='Не заполнен знак зодиака'
        )

    result = await get_horoscope(user_zodiac)
    return result
