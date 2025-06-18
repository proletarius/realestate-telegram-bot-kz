from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

router = Router()

@router.message(Command("subscribe"))
async def subscribe_handler(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить подписку", url="https://botpay.me/YOUR_LINK")]
        ]
    )

    await message.answer(
        "💳 <b>Премиум-подписка</b>\n\n"
        "✅ Все объявления без ограничений\n"
        "✅ Уведомления без задержек\n"
        "✅ Поддержка и приоритетная рассылка\n\n"
        "Стоимость: <b>1490 ₸ / месяц</b>\n\n"
        "Нажми кнопку ниже, чтобы оплатить 👇",
        reply_markup=kb
    )
