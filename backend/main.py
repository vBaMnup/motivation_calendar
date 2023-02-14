from api.api import img_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(img_router)
