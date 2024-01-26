from pydantic import BaseModel


class User(BaseModel):
    tg_id: int
    username: str
    zodiac: str = None
    count_request_calendar: int = 0
    count_request_horoscope: int = 0
    is_subscriber: bool = False
    is_quote_subscribe: bool = False
    is_horoscope_subscribe: bool = False

    class Config:
        arm_mode = True
        schema_extra = {"required": ["tg_id", "username"]}
        indexes = [{"fields": ["tg_id"], "unique": True}]


class Zodiac(BaseModel):
    zodiac: str
