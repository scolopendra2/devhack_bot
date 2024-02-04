from aiogram.dispatcher.filters.state import State, StatesGroup


def check(text):
    if '-' not in text:
        return False, 'В тексте отсутствует "-", попробуйте снова'
    text = text.split('-')
    if len(text) != 2:
        return False, 'В тексте больше одного "-", попробуйте снова'
    one_number, two_number = text
    if not one_number.isdigit() or not two_number.isdigit():
        return False, 'Текст должен содержать цифры и знак "-"'
    if int(two_number) < int(one_number):
        return False, 'Первое число должно быть больше второго'
    return True, [one_number, two_number]


class Add(StatesGroup):
    apartaments = State()
    padik = State()
    parkings = State()


class Change(StatesGroup):
    sec_id = State()
    login = State()
    password = State()
