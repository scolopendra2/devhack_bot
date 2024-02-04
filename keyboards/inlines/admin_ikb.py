from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db
from models import Employee

cancel_add_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена❌', callback_data='cancel_add'),
        ]
    ],
    resize_keyboard=True,
)

cancel_enter_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена❌', callback_data='cancel_enter'),
        ]
    ],
    resize_keyboard=True,
)

security_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить➕', callback_data='add_security'
            ),
            InlineKeyboardButton(
                text='Удалить❌', callback_data='delete_security'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Редактировать✏️', callback_data='edit_security'
            )
        ],
    ],
    resize_keyboard=True,
)

cancel_security_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='cancel_security'
            ),
        ]
    ],
    resize_keyboard=True,
)


def security_list_delete():
    employees = db.query(Employee).filter(Employee.is_admin == 0).all()
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
    )
    for employee in employees:
        ikb.add(
            InlineKeyboardButton(
                text=f'{employee.surname} {employee.name}',
                callback_data=f'delete_security_{employee.id}',
            )
        )
    return ikb


def security_list_edit():
    employees = db.query(Employee).filter(Employee.is_admin == 0).all()
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
    )
    for employee in employees:
        ikb.add(
            InlineKeyboardButton(
                text=f'{employee.surname} {employee.name}',
                callback_data=f'security_edit_{employee.id}',
            )
        )
    return ikb


def create_for_edit(security_id):
    change_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить логин✏️',
                    callback_data=f'login_edit_{security_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Изменить пароль✏️',
                    callback_data=f'password_edit_{security_id}',
                )
            ],
            [
                InlineKeyboardButton(
                    text='Отмена❌', callback_data='cancel_security'
                ),
            ],
        ],
        resize_keyboard=True,
    )
    return change_ikb
