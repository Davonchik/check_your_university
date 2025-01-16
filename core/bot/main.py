import asyncio
from aiogram import Bot, Dispatcher, types, F
from config import settings
from aiogram.filters import CommandStart
from api_client import APIClient
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.reply_keyboards import main_keyboard
from keyboards.inline_keyboards import category_keyboard
#from ..logger import logger


dp = Dispatcher()
api_client = APIClient(settings.API_BASE_URL)

class Request(StatesGroup):
    building_name = State()
    category = State()
    room = State()
    text = State()
    photo = State()
    wait_category = State()
    

@dp.message(CommandStart())
async def start(message: types.Message):
    #logger.info("Start bot")
    user = await api_client.create_user(str(message.from_user.id))
    #await state.set_state(Request.building_name)
    print(user)
    await message.answer(
        "Hello, I'm a bot! Choose an option below:", 
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.text == "About us")
async def about_us(message: types.Message):
    #logger.info("About us")
    # Отправляем текст о компании
    await message.answer(
        "We are a company that values innovation and quality. "
        "Our mission is to provide the best services for our clients."
    )

@dp.message(lambda message: message.text == "Create a request")
async def create_request(message: types.Message, state: FSMContext):
    #logger.info("Create request")
    await state.set_state(Request.building_name)
    await message.answer("Let's create a request. Please enter the building name:")

@dp.message(Request.building_name)
async def building_name(message: types.Message, state: FSMContext):
    await state.update_data(building_name=message.text)
    await message.answer("Choose category", reply_markup=category_keyboard)
    await state.set_state(Request.wait_category)
    #logger.info("Building name: %s", message.text)


@dp.callback_query(Request.wait_category, F.data.in_({
    "clean", "equipment", "light", "temperature", 
    "noise", "tech", "access", "sanitary", 
    "comfort", "other"
}))
async def category(callback_query: types.CallbackQuery, state: FSMContext):
    category_map = {
        "clean": "Чистота и гигиена",
        "equipment": "Оборудование",
        "light": "Освещение",
        "temperature": "Температура и климат",
        "noise": "Шум и звукоизоляция",
        "tech": "Техническое состояние",
        "access": "Доступность",
        "sanitary": "Санитарные узлы",
        "comfort": "Эстетика и комфорт",
        "other": "Другое",
    }
    category_name = category_map[callback_query.data]
    await state.update_data(category=category_name)
    await state.set_state(Request.room)
    await callback_query.message.edit_text(f"Selected category: {category_name}")
    await callback_query.message.answer("Enter room")
    # logger.info("Category: %s", callback_query.data)

@dp.message(Request.room)
async def room(message: types.Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(Request.text)
    await message.answer("Enter text")
    #logger.info("Room: %s", message.text)

@dp.message(Request.text)
async def text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Request.photo)
    await message.answer("Enter photo url")
    #logger.info("Text: %s", message.text)

@dp.message(Request.photo)
async def photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_url=message.text)
    data = await state.get_data()
    data["user_id"] = message.from_user.id
    await api_client.create_request(data)
    await message.answer("Request created")
    #logger.info("Photo: %s", message.text)
    await state.clear()
    

async def main():
    #logger.info("Starting bot")
    bot = Bot(token=settings.TG_KEY)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())