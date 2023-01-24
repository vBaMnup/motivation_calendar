from fastapi import FastAPI

from api.api import img_router

app = FastAPI()

app.include_router(img_router)
