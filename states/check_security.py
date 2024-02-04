from aiogram.dispatcher.filters.state import State, StatesGroup


class CheckGos(StatesGroup):
    gos = State()
