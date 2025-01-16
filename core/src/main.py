from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api.middleware import AuthMiddleware

from src.presentation.api.request import router_request
from src.presentation.api.user import router_user
from src.presentation.api.admin import router_admin
from src.presentation.api.admin_actions import router_admin_actions
from check_your_university.core.src.presentation.api.s3 import s3_router

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
app.include_router(router_admin_actions)
app.include_router(s3_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(
    AuthMiddleware,
    prefixes=[
        router_admin_actions.prefix
    ]
)

@app.get("/")
async def root():
    logger.info("Обработан запрос на корневой маршрут")
    return {"message": "root"}