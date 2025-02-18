import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from src.handlers import router
from src.middlewares.antiflood import ThrottlingMiddleware
from src.middlewares.logging_for_bot import LoggingMiddleware

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.middleware(LoggingMiddleware())
dp.message.middleware(ThrottlingMiddleware())
dp.callback_query.middleware(ThrottlingMiddleware())

dp.include_router(router)

# Функция для запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True) # Запросы отправленные боту когда он был в оффлайне
                                                        # не обрабатываются
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        raise e
