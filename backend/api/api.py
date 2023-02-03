from fastapi import APIRouter, HTTPException

from pictures.pic_maker import CreateImage
from .models import users
from .schema import User

img_router = APIRouter()


@img_router.post("/users/")
async def create_user(user: User):
    """
    Создание нового пользователя
    """
    if users.find_one({'tg_id': user.tg_id}):
        raise HTTPException(
            status_code=400,
            detail='Такой пользователь уже существует'
        )
    user_data = {
        "tg_id": user.tg_id,
        "username": user.username,
        "zodiac": user.zodiac,
        "count_request": 0,
        "is_subscriber": False
    }
    users.insert_one(user_data)
    return {"tg_id": user.tg_id, "username": user.username}


@img_router.put("/users/{tg_id}/zodiac")
async def update_user_zodiac(tg_id: int, zodiac: str):
    """
    Обновление знака зодиака пользователя
    """
    result = users.update_one({"tg_id": tg_id}, {"$set": {"zodiac": zodiac}})
    return {"result": "Zodiac updated"} if result.modified_count else {
        "result": "User not found"
    }


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
async def get_calendar(tg_id: int):
    user_data = users.find_one({'tg_id': tg_id})
    if user_data is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if (user_data.get('count_request') > 0
            and not user_data.get('is_subscriber')):
        raise HTTPException(
            status_code=400,
            detail='Пользователь без активной подписки может делать только 1 '
                   'запрос в месяц'
        )

    users.update_one({'tg_id': tg_id}, {'$inc': {'count_request': 1}})

    return {
        'file_link': CreateImage().make_wallpaper(
            tg_id,
            user_data.get('zodiac')
        )
    }
