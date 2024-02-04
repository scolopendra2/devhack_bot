from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db
from models import Employee

cancel_check_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='cancel_check_number'
            ),
        ]
    ],
    resize_keyboard=True,
)
