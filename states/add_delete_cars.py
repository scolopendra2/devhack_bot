from aiogram.dispatcher.filters.state import State, StatesGroup


class AddDeleteCars(StatesGroup):
    number_car = State()


class AddDeleteCarsGuest(StatesGroup):
    number_car = State()
    alive = State()
