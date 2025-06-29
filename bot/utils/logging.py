import logging
import asyncio
import os
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Чтение из .env
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram-бот для отправки ошибок
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# 📁 Убедимся, что папка logs существует
os.makedirs("logs", exist_ok=True)

# 📝 Логгер, пишущий в файл
file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

# 🔁 Telegram-логгер
class TelegramErrorHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR and ADMIN_ID:
            log_entry = self.format(record)
            asyncio.create_task(self.send_to_admin(log_entry))

    async def send_to_admin(self, text: str):
        try:
            await bot.send_message(ADMIN_ID, f"❗️<b>Ошибка:</b>\n<pre>{text}</pre>", parse_mode=ParseMode.HTML)
        except Exception as e:
            print("⚠️ Не удалось отправить ошибку админу:", e)

# Функция для настройки логирования
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Добавляем лог в файл
    logger.addHandler(file_handler)

    # Добавляем Telegram для ERROR
    telegram_handler = TelegramErrorHandler()
    telegram_handler.setLevel(logging.ERROR)
    telegram_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(telegram_handler)
