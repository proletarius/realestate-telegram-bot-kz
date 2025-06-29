import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def set_bot_commands():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    commands = [
        BotCommand(command="start", description="🔍 Начать поиск"),
        BotCommand(command="filter", description="⚙️ Изменить фильтр"),
        BotCommand(command="myfilter", description="🔎 Посмотреть текущий фильтр"),
        BotCommand(command="subscribe", description="💳 Подписка"),
        BotCommand(command="help", description="📘 Помощь"),
    ]

    await bot.set_my_commands(commands)
    await bot.session.close()
    print("✅ Меню установлено")

if __name__ == "__main__":
    asyncio.run(set_bot_commands())
