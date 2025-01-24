from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from fastapi_server.orm import ItemOrm
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

message_router = Router()
search_button = KeyboardButton(text="Найти по артикулу")
kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[search_button]])


class Search(StatesGroup):
    article = State()


@message_router.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(text="Привет", reply_markup=kb)


@message_router.message(F.text == "Найти по артикулу")
async def introduction(message: Message, state: FSMContext):
    await state.set_state(Search.article)
    await message.answer("Введите артикул")


@message_router.message(Search.article)
async def get_item_by_article(message: Message, state: FSMContext):
    try:
        text = int(message.text)
    except:
        await message.answer("Введите корректный артикул")
        return
    item = await ItemOrm.get_item(text)
    if item is None:
        await message.answer("Товар не найден")
        return
    await message.answer(
        f"Товар найден\nнаименование: {item.name}\nартикул: {item.article}\nцена: {item.price}\nколичество: {item.amount}\nрейтинг: {item.rating}"
    )
    await state.clear()


@message_router.message()
async def echo(message: Message):
    await message.answer(text="Неизвестная команда. Введите /start.")
