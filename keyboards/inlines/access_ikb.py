from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db
from models import Car, Resident

all_access_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='car_add'),
            InlineKeyboardButton(text='Удалить', callback_data='car_delete'),
        ],
        [InlineKeyboardButton(text='Список', callback_data='car_list')],
    ],
    resize_keyboard=True,
)
cancel_all_access_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='all_access_cancel'
            ),
        ]
    ],
    resize_keyboard=True,
)


def delete_all_ikb(tg_user_id):
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
    )
    resident = (
        db.query(Resident).filter(Resident.tg_user_id == tg_user_id).first()
    )
    numbers = (
        db.query(Car)
        .filter(Car.resident_id == resident.id, Car.date_end == None)
        .all()
    )
    for number in numbers:
        ikb.add(
            InlineKeyboardButton(
                text=number.gos_number, callback_data=f'cardelete_{number.id}'
            )
        )
    return ikb


guest_access_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить', callback_data='guest_car_add'
            ),
            InlineKeyboardButton(
                text='Удалить', callback_data='guest_car_delete'
            ),
        ],
        [InlineKeyboardButton(text='Список', callback_data='guest_car_list')],
    ],
    resize_keyboard=True,
)

alive_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1 час', callback_data='hour_1'),
            InlineKeyboardButton(text='3 часа', callback_data='hour_3'),
        ],
        [
            InlineKeyboardButton(text='7 часов', callback_data='hour_7'),
            InlineKeyboardButton(text='12 часов', callback_data='hour_12'),
        ],
        [InlineKeyboardButton(text='24 часа', callback_data='hour_24')],
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='guest_access_cancel'
            )
        ],
    ],
    resize_keyboard=True,
)

cancel_guest_access_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='guest_access_cancel'
            ),
        ]
    ],
    resize_keyboard=True,
)


def delete_guesst_ikb(tg_user_id):
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
    )
    resident = (
        db.query(Resident).filter(Resident.tg_user_id == tg_user_id).first()
    )
    numbers = (
        db.query(Car)
        .filter(Car.resident_id == resident.id, Car.date_end != None)
        .all()
    )
    for number in numbers:
        ikb.add(
            InlineKeyboardButton(
                text=number.gos_number,
                callback_data=f'guestdelete_{number.id}',
            )
        )
    return ikb
