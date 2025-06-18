from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from db.models import User
from db.database import AsyncSessionLocal
from bot.states.search_filter import SearchFilter

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=username)
            session.add(user)
            await session.commit()

    await message.answer("👋 Привет! Давай подберём фильтры для поиска квартиры. В каком городе ищем?")
    await state.set_state(SearchFilter.city)
