import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pathlib import Path
from telegram_bot.handlers import message_router
import os

load_dotenv(Path(__file__).resolve().parent / ".env")
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(message_router)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
