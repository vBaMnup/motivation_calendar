from pydantic import BaseModel


class User(BaseModel):
    tg_id: int
    username: str
    zodiac: str = None
    count_request: int = 0
    is_subscriber: bool = False

    class Config:
        arm_mode = True
        schema_extra = {
            "required": ["tg_id", "username"]
        }


class Zodiac(BaseModel):
    zodiac: str
