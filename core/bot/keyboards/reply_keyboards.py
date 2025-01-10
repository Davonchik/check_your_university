from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="About us")],
    [KeyboardButton(text="Create a request")]
], resize_keyboard=True, input_field_placeholder="Action Menu")