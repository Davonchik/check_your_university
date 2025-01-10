import asyncio
from aiogram import Bot, Dispatcher, types
from config import settings
from aiogram.filters import CommandStart
from api_client import APIClient
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.reply_keyboards import main_keyboard


dp = Dispatcher()
api_client = APIClient(settings.API_BASE_URL)

class Request(StatesGroup):
    building_name = State()
    category = State()
    room = State()
    text = State()
    photo = State()
    

@dp.message(CommandStart())
async def start(message: types.Message):
    user = await api_client.create_user(str(message.from_user.id))
    #await state.set_state(Request.building_name)
    print(user)
    await message.answer(
        "Hello, I'm a bot! Choose an option below:", 
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.text == "About us")
async def about_us(message: types.Message):
    # Отправляем текст о компании
    await message.answer(
        "We are a company that values innovation and quality. "
        "Our mission is to provide the best services for our clients."
    )

@dp.message(lambda message: message.text == "Create a request")
async def create_request(message: types.Message, state: FSMContext):
    await state.set_state(Request.building_name)
    await message.answer("Let's create a request. Please enter the building name:")

@dp.message(Request.building_name)
async def building_name(message: types.Message, state: FSMContext):
    await state.update_data(building_name=message.text)
    await state.set_state(Request.category)
    await message.answer("Enter category")

@dp.message(Request.category)
async def category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(Request.room)
    await message.answer("Enter room")

@dp.message(Request.room)
async def room(message: types.Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(Request.text)
    await message.answer("Enter text")

@dp.message(Request.text)
async def text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Request.photo)
    await message.answer("Enter photo url")

@dp.message(Request.photo)
async def photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_url=message.text)
    data = await state.get_data()
    await api_client.create_request(data)
    await message.answer("Request created")
    await state.clear()
    

async def main():
    bot = Bot(token=settings.TG_KEY)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())