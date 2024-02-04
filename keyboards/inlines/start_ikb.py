from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Регистрация', callback_data='register_resident'
            ),
            InlineKeyboardButton(
                text='Вход(для сотрудников УК)', callback_data='enter_employee'
            ),
        ]
    ],
    resize_keyboard=True,
)
