from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.modules.start.keyboards import start_keyboard


router = Router()


WELCOME_MESSAGE = "👋 Добро пожаловать в ServiceFlow\nВыберите действие:"


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        text=WELCOME_MESSAGE,
        reply_markup=start_keyboard(),
    )