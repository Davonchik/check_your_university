from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TG_KEY: str = '7999109509:AAHWr1xadrAoA1IthlhNjnJzOMQ0XKho7Qo'
    API_BASE_URL: str = "http://application_container:7777"



settings = Settings()