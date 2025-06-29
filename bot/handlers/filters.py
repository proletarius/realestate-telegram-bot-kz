from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.states.search_filter import SearchFilter
from bot.keyboards.inline import rooms_keyboard, property_type_keyboard, operation_type_keyboard, land_type_keyboard, year_built_keyboard, skip_search_text_keyboard, filter_saved_keyboard
from db.models import Preference
from db.database import AsyncSessionLocal
from sqlalchemy import delete

from bot.utils.save_filter import save_filter

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
        await message.answer("🛏 Сколько комнат?", reply_markup=rooms_keyboard()) # содержит "Не важно"
        await state.set_state(SearchFilter.rooms)
    except ValueError: 
        await message.answer("🚫 Пожалуйста, введите только цифры — например: 200000")


@router.callback_query(SearchFilter.rooms, F.data.startswith("room_"))
async def room_selected(callback: CallbackQuery, state: FSMContext):
    room_raw = callback.data.split("_")[1]
    rooms = None if room_raw == "x" else (4 if room_raw == "4" else int(room_raw))

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
    await callback.message.edit_reply_markup()

    if prop_type == "дом":
        from bot.keyboards.inline import land_type_keyboard
        await callback.message.answer("📄 Назначение участка:", reply_markup=land_type_keyboard())
        await state.set_state(SearchFilter.land_type)
    else:
        await callback.message.answer(
            "🔍 Введи ключевые слова для поиска (например: \"с ремонтом\") или нажми 🤷 Не важно:",
            reply_markup=skip_search_text_keyboard()
            )
        await state.set_state(SearchFilter.search_text)

    await callback.answer()


@router.callback_query(SearchFilter.land_type, F.data.startswith("land_"))
async def land_type_selected(callback: CallbackQuery, state: FSMContext):
    val = callback.data.split("_")[1]
    await state.update_data(land_type="ИЖС" if val == "izh" else None)

    from bot.keyboards.inline import year_built_keyboard
    await callback.message.edit_reply_markup()
    await callback.message.answer("🏗 Укажи год постройки дома:", reply_markup=year_built_keyboard())
    await state.set_state(SearchFilter.year_built)
    await callback.answer()


@router.callback_query(SearchFilter.year_built, F.data.startswith("year_"))
async def year_built_selected(callback: CallbackQuery, state: FSMContext):
    val = callback.data.split("_")[1]
    await state.update_data(year_built=int(val) if val != "x" else None)

    await callback.message.edit_reply_markup()
    await callback.message.answer(
        "🔍 Введи ключевые слова для поиска (например: \"с ремонтом\") или нажми 🤷 Не важно:",
        reply_markup=skip_search_text_keyboard()
        )
    await state.set_state(SearchFilter.search_text)
    await callback.answer()


@router.callback_query(SearchFilter.search_text, F.data == "text_x")
async def skip_search_text(callback: CallbackQuery, state: FSMContext):
    await state.update_data(search_text=None)
    await callback.message.edit_reply_markup()

    await save_filter(callback.from_user.id, state)
    
    await callback.message.answer(
        "✅ Фильтр сохранён! Я начну присылать тебе объявления, как только появятся подходящие.",
        reply_markup=filter_saved_keyboard()
        )
    
    await state.clear()
    await callback.answer()


@router.message(SearchFilter.search_text)
async def set_search_text(message: types.Message, state: FSMContext):
    await state.update_data(search_text=message.text)
    await save_filter(message.from_user.id, state)
    
    await message.answer(
        "✅ Фильтр сохранён! Я начну присылать тебе объявления, как только появятся подходящие.",
        reply_markup=filter_saved_keyboard()
        )
 
    await state.clear()