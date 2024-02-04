from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_resident_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='cancel_resident'
            ),
        ]
    ],
    resize_keyboard=True,
)
