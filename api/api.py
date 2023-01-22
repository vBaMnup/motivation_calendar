from fastapi import APIRouter

from .schema import User
from pictures.pic_maker import CreateImage

img_router = APIRouter()


@img_router.post("/get_calendar")
async def get_calendar(user: User):
    return CreateImage().make_wallpaper(), "OK"

