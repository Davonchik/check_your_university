from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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