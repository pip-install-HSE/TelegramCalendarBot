from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    name = State()
    phone = State()
    day = State()
    month = State()
    year = State()
    time = State()
