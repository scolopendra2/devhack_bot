from aiogram.dispatcher.filters.state import State, StatesGroup


class EnterEmployee(StatesGroup):
    login = State()
    password = State()
