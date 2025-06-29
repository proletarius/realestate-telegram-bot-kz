from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from db.database import AsyncSessionLocal
from db.models import Preference
from bot.keyboards.inline import edit_or_delete_filter_keyboard
from aiogram import Router

router = Router()

@router.message(Command("myfilter"))
async def show_my_filter_message(message: Message):
    await show_my_filter(message)


@router.callback_query(lambda c: c.data == "view_filter")
async def show_my_filter_callback(callback: CallbackQuery):
    await show_my_filter(callback)
    await callback.answer()

async def show_my_filter(event: Message | CallbackQuery):
    user_id = event.from_user.id

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Preference.__table__.select().where(Preference.user_id == user_id)
        )
        pref = result.fetchone()

    if not pref:
        if isinstance(event, CallbackQuery):
            await event.message.answer("⚠️ У тебя пока нет активного фильтра. Используй /filter чтобы настроить.")
        else:
            await event.answer("⚠️ У тебя пока нет активного фильтра. Используй /filter чтобы настроить.")
        return

    data = pref._mapping

    text = (
        "<b>🔎 Твой текущий фильтр:</b>\n"
        f"📍 Город: <b>{data.get('city') or '-'}</b>\n"
        f"📦 Сделка: <b>{data.get('operation_type') or '-'}</b>\n"
        f"🏠 Тип: <b>{data.get('property_type') or '-'}</b>\n"
        f"💰 До: <b>{data.get('max_price') or '—'} ₸</b>\n"
        f"🛏 Комнат: <b>{data.get('rooms') or 'Не важно'}</b>\n"
        f"📋 Ключевые слова: <b>{data.get('search_text') or 'Нет'}</b>\n"
        f"🏡 Назначение участка: <b>{data.get('land_type') or 'Не важно'}</b>\n"
        f"📆 Год постройки: <b>{data.get('year_built') or 'Не важно'}</b>\n"
    )

    short_text = text[:4000]  # безопасно, но почти лимит

    if isinstance(event, CallbackQuery):
        await event.message.answer(short_text, reply_markup=edit_or_delete_filter_keyboard())
    else:
        await event.answer(short_text, reply_markup=edit_or_delete_filter_keyboard())

@router.callback_query(lambda c: c.data == "delete_filter")
async def delete_filter_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        await session.execute(
            Preference.__table__.delete().where(Preference.user_id == user_id)
        )
        await session.commit()

    await callback.message.edit_reply_markup()
    await callback.message.answer("🗑 Фильтр удалён. Используй /filter чтобы создать новый.")
    await callback.answer()
