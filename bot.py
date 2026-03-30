import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.translate import router

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Token topilmadi! .env faylni tekshir")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Bot ishga tushdi! To'xtatish uchun Ctrl+C bosing.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())