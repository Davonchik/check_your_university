from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from core.src.application.services.request_service import get_requests
from config import settings
from api_client import APIClient

api_client = APIClient(settings.API_BASE_URL)

category_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Чистота и гигиена", callback_data="clean")],
    [InlineKeyboardButton(text="Оборудование", callback_data="equipment")],
    [InlineKeyboardButton(text="Освещение", callback_data="light")],
    [InlineKeyboardButton(text="Температура и климат", callback_data="temperature")],
    [InlineKeyboardButton(text="Шум и звукоизоляция", callback_data="noise")],
    [InlineKeyboardButton(text="Техническое состояние", callback_data="tech")],
    [InlineKeyboardButton(text="Доступность", callback_data="access")],
    [InlineKeyboardButton(text="Санитарные узлы", callback_data="sanitary")],
    [InlineKeyboardButton(text="Эстетика и комфорт", callback_data="comfort")],
    [InlineKeyboardButton(text="Другое", callback_data="other")],
])

yes_no_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes")],
    [InlineKeyboardButton(text="Нет", callback_data="no")],
])

async def get_unique_building_names_keyboard():
    buildings = await api_client.get_buildings()
    buttons = []
    for building in buildings:
        building_name = f"{building}"
        buttons.append([InlineKeyboardButton(text=building_name, callback_data=building_name)])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
