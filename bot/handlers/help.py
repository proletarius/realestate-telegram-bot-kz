from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📘 <b>Что умеет этот бот:</b>\n\n"
        "🏠 Я нахожу новые объявления по недвижимости (аренда/покупка) из Krisha.kz и Olx.kz\n"
        "⚡ Присылаю их первым — прямо в Telegram\n"
        "🔍 Ты можешь задать фильтр по городу, цене, количеству комнат и типу жилья\n\n"
        "💳 <b>Подписка:</b>\n"
        "— Бесплатно: до 3 объявлений в день\n"
        "— Премиум: все релевантные объявления без ограничений\n\n"
        "🛠 <b>Команды:</b>\n"
        "/start — задать фильтр\n"
        "/help — справка\n"
        "/filter — изменить фильтр\n"
        "/subscribe — оформить подписку\n\n"
        "Если возникли вопросы — просто напиши сюда 👍"
    )
