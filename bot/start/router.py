from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

from start.service import telegram_api_activate

router = Router()


WELCOME_MESSAGE = "👋 Добро пожаловать в ServiceFlow\nВыберите действие:"


@router.message(CommandStart())
async def start_handler(
        message: Message,
        command: CommandObject
):
    token = command.args

    if not token:
        await message.answer(
            "Для подключения аккаунта перейдите по ссылке из ServiceFlow"
        )
        return

    telegram_id = message.from_user.id

    result = await telegram_api_activate(
        token=token,
        telegram_id=telegram_id
    )

    if result:
        await message.answer(
            "Ваш аккаунт ServiceFlow успешно подключён!"
        )

    else:
        await message.answer(
            "Ссылка недействительна или срок её действия истёк."
        )


