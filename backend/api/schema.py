from pydantic import BaseModel


class User(BaseModel):
    name: str
    zodiac: str
    is_subscriber: bool
