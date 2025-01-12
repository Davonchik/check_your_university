from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.request import router_request
from src.presentation.api.user import router_user
from src.presentation.api.admin import router_admin

from src.logger import logger




@asynccontextmanager
async def lifespan(_):
    logger.info("Приложение запускается...")
    yield
    logger.info("Приложение остановлено")


app = FastAPI(title='Test', description='Test API', version='1.0.0', lifespan=lifespan)
app.include_router(router_request)
app.include_router(router_user)
app.include_router(router_admin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
async def root():
    logger.info("Обработан запрос на корневой маршрут")
    return {"message": "root"}