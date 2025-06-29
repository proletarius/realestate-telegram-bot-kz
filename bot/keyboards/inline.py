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
         [InlineKeyboardButton(text="🤷 Не важно", callback_data="room_x")],
    ])

def property_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Квартира", callback_data="type_flat")],
        [InlineKeyboardButton(text="🏡 Дом", callback_data="type_house")],
    ])

def land_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏡 ИЖС", callback_data="land_izh")],
        [InlineKeyboardButton(text="🤷 Не важно", callback_data="land_x")]
    ])

def year_built_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1970+", callback_data="year_1970"),
            InlineKeyboardButton(text="1980+", callback_data="year_1980")
        ],
        [
            InlineKeyboardButton(text="1990+", callback_data="year_1990"),
            InlineKeyboardButton(text="2000+", callback_data="year_2000")
        ],
        [
            InlineKeyboardButton(text="🤷 Не важно", callback_data="year_x")
        ]
    ])

def skip_search_text_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤷 Не важно", callback_data="text_x")]
    ])

def filter_saved_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Посмотреть фильтр", callback_data="view_filter")]
    ])

def edit_or_delete_filter_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="♻️ Изменить фильтр", callback_data="edit_filter"),
            InlineKeyboardButton(text="🗑 Удалить фильтр", callback_data="delete_filter")
        ]
    ])