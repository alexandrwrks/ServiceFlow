import asyncio

from aiogram import Bot, Dispatcher

from start.router import router as start_router
from bot_utils.settings import settings


async def starting_bot():
    bot = Bot(settings.BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)

    print("Starting bot...")

    bot_info = await bot.get_me()

    print(bot_info.username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(starting_bot())
    except KeyboardInterrupt:
        print("Stopping bot...")
