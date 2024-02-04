from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

agree_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Согласиться✅', callback_data='agree')]
    ],
    resize_keyboard=True,
)
