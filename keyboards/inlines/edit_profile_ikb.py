from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

edit_profile_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Изменить фамилию✏️', callback_data='surname_edit'
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить имя✏️', callback_data='name_edit'
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить отчество✏️', callback_data='patronymic_edit'
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить номер телефона✏️',
                callback_data='phone_number_edit',
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить квартиру✏️',
                callback_data='number_appartament_edit',
            )
        ],
        [
            InlineKeyboardButton(
                text='Изменить номер парковочного места✏️',
                callback_data='number_place_edit',
            )
        ],
    ],
    resize_keyboard=True,
)

cancel_edit_profile_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='cancel_edit_profile'
            ),
        ]
    ],
    resize_keyboard=True,
)
