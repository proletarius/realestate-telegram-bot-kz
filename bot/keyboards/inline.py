from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def operation_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Аренда", callback_data="op_rent")],
        [InlineKeyboardButton(text="🏡 Покупка", callback_data="op_buy")],
    ])

def rooms_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1", callback_data="room_1"),
         InlineKeyboardButton(text="2", callback_data="room_2")],
        [InlineKeyboardButton(text="3", callback_data="room_3"),
         InlineKeyboardButton(text="4+", callback_data="room_4")],
    ])

def property_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Квартира", callback_data="type_flat")],
        [InlineKeyboardButton(text="🏡 Дом", callback_data="type_house")],
    ])