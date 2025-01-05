from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infrastructure.routes import request


@asynccontextmanager
async def lifespan(_):
    print('start')
    yield
    print('stop')


app = FastAPI(title='Test', description='Test API', version='1.0.0', lifespan=lifespan)
app.include_router(request.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
async def root():
    return {"message": "root"}