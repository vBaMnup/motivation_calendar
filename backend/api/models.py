from settings.config import MONGO_CLIENT

db = MONGO_CLIENT["TG_USER_DATABASE"]
users = db["users"]

users.create_index("tg_id", unique=True)
