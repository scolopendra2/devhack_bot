from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить квартиры'),
            KeyboardButton(text='Добавить парковочные места'),
        ],
        [KeyboardButton(text='Охрана')],
    ],
    resize_keyboard=True,
)
