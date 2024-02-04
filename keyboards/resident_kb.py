from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_resident_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Редактировать профиль')],
        [
            KeyboardButton(text='Постоянный доступ'),
            KeyboardButton(text='Гостевой доступ'),
        ],
    ],
    resize_keyboard=True,
)
