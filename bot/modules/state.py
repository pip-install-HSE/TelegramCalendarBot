from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    name = State()
    phone = State()
    month = State()
    day = State()
    time = State()
