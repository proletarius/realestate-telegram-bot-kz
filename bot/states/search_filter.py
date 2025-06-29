from aiogram.fsm.state import StatesGroup, State

class SearchFilter(StatesGroup):
    city = State()
    operation_type = State()
    max_price = State()
    rooms = State()
    property_type = State()
    land_type = State()       # только для домов
    year_built = State()      # только для домов
    search_text = State()
