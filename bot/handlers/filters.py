from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.search_filter import SearchFilter
from bot.keyboards.inline import rooms_keyboard, property_type_keyboard, operation_type_keyboard
from db.models import Preference
from db.database import AsyncSessionLocal


router = Router()

@router.message(SearchFilter.city)
async def set_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("📄 Выбери тип сделки:", reply_markup=operation_type_keyboard())
    await state.set_state(SearchFilter.operation_type)


@router.callback_query(SearchFilter.operation_type, F.data.startswith("op_"))
async def set_operation_type(callback: CallbackQuery, state: FSMContext):
    op_raw = callback.data.split("_")[1]
    operation_type = "аренда" if op_raw == "rent" else "покупка"

    await state.update_data(operation_type=operation_type)
    await callback.message.edit_reply_markup()
    await callback.message.answer("💰 Максимальная цена?")
    await state.set_state(SearchFilter.max_price)
    await callback.answer()


@router.message(SearchFilter.max_price)
async def set_max_price(message: types.Message, state: FSMContext):
    try:
        max_price = int(message.text.replace(" ", ""))
        await state.update_data(max_price=max_price)
        await message.answer("🛏 Сколько комнат?", reply_markup=rooms_keyboard())
        await state.set_state(SearchFilter.rooms)
    except ValueError: 
        await message.answer("🚫 Пожалуйста, введите только цифры — например: 200000")


@router.callback_query(SearchFilter.rooms, F.data.startswith("room_"))
async def room_selected(callback: CallbackQuery, state: FSMContext):
    room_raw = callback.data.split("_")[1]
    rooms = 4 if room_raw == "4" else int(room_raw)

    await state.update_data(rooms=rooms)
    await callback.message.edit_reply_markup(reply_markup=None)  # убираем клаву
    await callback.message.answer("🏠 Что ищем?", reply_markup=property_type_keyboard())
    await state.set_state(SearchFilter.property_type)
    await callback.answer()  # закрывает "часики"


@router.callback_query(SearchFilter.property_type, F.data.startswith("type_"))
async def property_type_selected(callback: CallbackQuery, state: FSMContext):
    prop_raw = callback.data.split("_")[1]
    prop_type = "квартира" if prop_raw == "flat" else "дом"

    await state.update_data(property_type=prop_type)

    # Сохраняем всё в БД
    data = await state.get_data()
    from db.models import Preference
    from db.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        pref = Preference(
            user_id=callback.from_user.id,
            city=data["city"],
            operation_type=data["operation_type"],
            max_price=data["max_price"],
            rooms=data["rooms"],
            property_type=prop_type
        )
        session.add(pref)
        await session.commit()

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("✅ Фильтр сохранён! Я начну присылать тебе объявления, как только появятся подходящие.")
    await state.clear()
    await callback.answer()