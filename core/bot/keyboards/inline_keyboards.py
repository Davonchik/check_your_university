from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from core.src.application.services.request_service import get_requests

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

# async def get_unique_building_ids():
#     requests = await get_requests()  # Получение заявок
#     building_ids = {request["building_id"] for request in requests}  # Уникальные building_id
#     return building_ids

# async def get_unique_building_names_keyboard():
#     building_ids = await get_unique_building_ids()
#     keyboard = InlineKeyboardMarkup()
#     for building_id in building_ids:
#         building_name = f"Building {building_id}"  # Замените на правильное название здания
#         keyboard.add(InlineKeyboardButton(text=building_name, callback_data=building_name))
#     return keyboard
