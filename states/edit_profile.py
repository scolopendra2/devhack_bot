from aiogram.dispatcher.filters.state import State, StatesGroup


class EditProfile(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    phone_number = State()
    number_appartament = State()
    number_place = State()
