from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import start, filters, help, filter, subscribe
from dotenv import load_dotenv
import os, asyncio

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(filters.router)
    dp.include_router(help.router)
    dp.include_router(filter.router)
    dp.include_router(subscribe.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
