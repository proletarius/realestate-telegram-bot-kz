import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import start, filters, help, filter, subscribe, myfilter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from parser.distributor import send_ads_to_users
from bot.utils.logging import setup_logging  # обновлённая функция логирования

# Добавляем путь к корню проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

# Настройка логов и конфигурации
setup_logging()
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Подключение роутеров
dp.include_routers(
    start.router,
    filters.router,
    help.router,
    filter.router,
    subscribe.router,
    myfilter.router
)

async def on_startup():
    logger.info("✅ Бот и планировщик запущены")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_ads_to_users, trigger="interval", minutes=15)
    scheduler.start()

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
