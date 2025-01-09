from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TG_KEY: str
    API_BASE_URL: str = "http://localhost:7777"
    class Config:
        env_file = ".env"


settings = Settings()