import logging
from logging.handlers import RotatingFileHandler
import os

# Убедимся, что директория для логов существует
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Глобальный уровень логирования
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        RotatingFileHandler(
            os.path.join(LOG_DIR, "app.log"), maxBytes=10 * 1024 * 1024, backupCount=5
        ),  # Логирование в файл
        logging.StreamHandler(),  # Логирование в консоль
    ],
)

# Функция для создания именованных логгеров
def get_logger(name: str):
    """Возвращает логгер с заданным именем."""
    return logging.getLogger(name)
