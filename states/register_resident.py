from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterResident(StatesGroup):
    fio = State()
    phone_number = State()
    apartment_number = State()
    parking_number = State()
