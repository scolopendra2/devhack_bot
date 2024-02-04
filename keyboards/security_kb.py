from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_security_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список постоянных пропусков'),
            KeyboardButton(text='Список временных пропусков'),
        ],
        [KeyboardButton(text='Проверить номер')],
    ],
    resize_keyboard=True,
)
