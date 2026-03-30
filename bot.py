import asyncio
import logging
from os import getenv

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv

from handlers.translate import router

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
WEBHOOK_BASE_URL = getenv("WEBHOOK_BASE_URL")
PORT = int(getenv("PORT", "8000"))
WEBHOOK_PATH = "/webhook"

if not BOT_TOKEN:
    raise ValueError("Token topilmadi! .env faylni tekshir")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def healthcheck(_: web.Request) -> web.Response:
    return web.Response(text="Tarjima bot ishlayapti")


async def telegram_webhook(request: web.Request) -> web.Response:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return web.Response(text="OK")


async def on_startup(_: web.Application) -> None:
    await bot.set_webhook(f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}")
    me = await bot.get_me()
    logging.info("Webhook o'rnatildi: %s", f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}")
    logging.info("Bot ulandi: @%s", me.username)


async def on_shutdown(_: web.Application) -> None:
    await bot.delete_webhook()
    await bot.session.close()


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", healthcheck)
    app.router.add_post(WEBHOOK_PATH, telegram_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


async def run_polling() -> None:
    logging.info("Bot polling rejimida ishga tushdi")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    if WEBHOOK_BASE_URL:
        logging.info("Bot webhook rejimida ishga tushdi")
        web.run_app(create_app(), host="0.0.0.0", port=PORT)
        return

    asyncio.run(run_polling())


if __name__ == "__main__":
    main()
