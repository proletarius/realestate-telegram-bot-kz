from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.search_filter import SearchFilter

router = Router()

@router.message(F.text == "/filter")
async def change_filter(message: types.Message, state: FSMContext):
    await message.answer("🔄 Давай изменим фильтр. В каком городе ищем?")
    await state.clear()
    await state.set_state(SearchFilter.city)
