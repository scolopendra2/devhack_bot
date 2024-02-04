from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import (
    security_ikb,
    cancel_security_ikb,
    security_list_edit,
    security_list_delete,
    create_for_edit,
)
from loader import dp, db, bot
from models import Resident, Appartament, Parking, Employee
from states import RegisterSecurity, Change


@dp.callback_query_handler(text='cancel_security', state=RegisterSecurity)
async def cancel_security(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено')


@dp.callback_query_handler(text='cancel_security', state=Change)
async def cancel_security(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено')


@dp.message_handler(text='Охрана')
async def security(message: types.Message):
    admin = (
        db.query(Employee)
        .filter(
            Employee.tg_user_id == message.from_user.id, Employee.is_admin == 1
        )
        .first()
    )
    if admin is not None:
        await message.answer('Выберите действие', reply_markup=security_ikb)


@dp.callback_query_handler(text='add_security')
async def list_add_security(call: types.CallbackQuery):
    await call.message.answer(
        'Введите фио охранника', reply_markup=cancel_security_ikb
    )
    await RegisterSecurity.fio.set()


@dp.message_handler(content_types=['text'], state=RegisterSecurity.fio)
async def set_fio(message: types.Message, state: FSMContext):
    split_message = message.text.split()
    if len(split_message) != 3:
        await message.answer(
            'Введите настоящее ФИО', reply_markup=cancel_security_ikb
        )
    else:
        await state.update_data(fio=split_message)
        await message.answer(
            'Теперь пожалуйста пришлите мне номер телефона',
            reply_markup=cancel_security_ikb,
        )
        await RegisterSecurity.phone_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterSecurity.phone_number
)
async def set_phone_number(message: types.Message, state: FSMContext):
    symbols = list(message.text)
    number = ' '.join(list(map(lambda x: x.strip(), symbols)))
    resident = (
        db.query(Resident).filter(Resident.phone_number == number).first()
    )
    if len(list(filter(lambda x: x.isdigit(), symbols))) != 11:
        await message.answer(
            'Введите свой настоящий номер телефона',
            reply_markup=cancel_security_ikb,
        )
    elif resident is not None:
        await message.answer(
            'Номер телефона был замечен в базе жильцев, '
            'данные о квартире и парковочном месте подставились автоматически'
        )
        await message.answer(
            'Теперь пожалуйста придуймайте логин для входа в аккаунт',
            reply_markup=cancel_security_ikb,
        )
        await state.update_data(phone_number=number)
        await state.update_data(apartment_number=resident.apartment_id)
        await state.update_data(parking_number=resident.parking_id)
        await RegisterSecurity.login.set()
    else:
        await state.update_data(phone_number=number)
        await message.answer(
            'Теперь пожалуйста пришлите мне номер квартиры',
            reply_markup=cancel_security_ikb,
        )
        await RegisterSecurity.apartment_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterSecurity.apartment_number
)
async def apartment_number(message: types.Message, state: FSMContext):
    number_apartaments = message.text
    appartamentnts = db.query(Appartament).all()
    if number_apartaments not in list(
        map(lambda x: str(x.number_appartament), appartamentnts)
    ):
        await message.answer(
            'Квартиры нет в списке квартир дома попробуйте снова',
            reply_markup=cancel_security_ikb,
        )
    else:
        await state.update_data(apartment_number=number_apartaments)
        await message.answer(
            'Теперь пожалуйста пришлите мне номер парковочного места',
            reply_markup=cancel_security_ikb,
        )
        await RegisterSecurity.parking_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterSecurity.parking_number
)
async def parking_number(message: types.Message, state: FSMContext):
    number_parking = message.text
    parking_place = db.query(Parking).all()
    if number_parking not in list(
        map(lambda x: str(x.number_place), parking_place)
    ):
        await message.answer(
            'Такого парковочного места не существует попробуйте снова',
            reply_markup=cancel_security_ikb,
        )
    else:
        await state.update_data(parking_number=number_parking)
        await message.answer(
            'Теперь пожалуйста придуймайте логин для входа в аккаунт',
            reply_markup=cancel_security_ikb,
        )
        await RegisterSecurity.login.set()


@dp.message_handler(content_types=['text'], state=RegisterSecurity.login)
async def set_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer(
        'Теперь пожалуйста придуймайте пароль для входа в аккаунт',
        reply_markup=cancel_security_ikb,
    )
    await RegisterSecurity.password.set()


@dp.message_handler(content_types=['text'], state=RegisterSecurity.password)
async def set_login(message: types.Message, state: FSMContext):
    data = await state.get_data()
    employee = Employee()
    employee.login = data['login']
    employee.set_password(message.text)
    employee.parking_id = data['parking_number']
    employee.apartment_id = data['apartment_number']
    employee.phone_number = data['phone_number']
    resident = (
        db.query(Resident)
        .filter(Resident.phone_number == data['phone_number'])
        .first()
    )
    if resident is not None:
        employee.name = resident.name
        employee.surname = resident.surname
        employee.patronymic = resident.patronymic
        employee.tg_user_id = resident.tg_user_id
        await bot.send_message(
            chat_id=resident.tg_user_id,
            text='Вас сделали охранником вам доступен новый функционал',
        )
        db.delete(resident)
    else:
        surname, name, patronymic = data['fio']
        employee.name = name
        employee.surname = surname
        employee.patronymic = patronymic
    db.add(employee)
    db.commit()
    await state.finish()
    await message.answer('Охранник успешно создан')


@dp.callback_query_handler(text='delete_security')
async def delete_security(call: types.CallbackQuery):
    ikb = security_list_delete()
    await call.message.answer(
        'Выберите охранника которого хотите удалить', reply_markup=ikb
    )


@dp.callback_query_handler(lambda query: query.data.startswith('delete_'))
async def delete(call: types.CallbackQuery):
    id_delete = call.data.split('_')[2]
    employee = db.query(Employee).filter(Employee.id == id_delete).first()
    db.delete(employee)
    db.commit()
    await bot.send_message(
        text='У вас забрали роль охранника',
        chat_id=employee.tg_user_id,
        reply_markup=None,
    )
    await call.message.answer('Охранник успешно удалён')


@dp.callback_query_handler(text='edit_security')
async def edit_security(call: types.CallbackQuery):
    ikb = security_list_edit()
    await call.message.answer(
        'Выберите охранника которого хотите изменить', reply_markup=ikb
    )


@dp.callback_query_handler(
    lambda query: query.data.startswith('security_edit')
)
async def edit(call: types.CallbackQuery):
    id_security = call.data.split('_')[2]
    employee = db.query(Employee).filter(Employee.id == id_security).first()
    ikb = create_for_edit(id_security)
    await call.message.answer(
        f'Охранник: {employee.surname} {employee.name}\n'
        f'Логин: {employee.login}\n'
        f'Пароль: зашифрованная информация\n\n'
        f'Выберите что хотите изменить',
        reply_markup=ikb,
    )
    await Change.sec_id.set()


@dp.callback_query_handler(
    lambda query: query.data.startswith('login_edit'), state=Change.sec_id
)
async def login_edit(call: types.CallbackQuery, state: FSMContext):
    id_security = call.data.split('_')[2]
    await state.update_data(sec_id=id_security)
    await call.message.answer(
        'Введите новый логин', reply_markup=cancel_security_ikb
    )
    await Change.login.set()


@dp.callback_query_handler(
    lambda query: query.data.startswith('password_edit_'), state=Change.sec_id
)
async def login_edit(call: types.CallbackQuery, state: FSMContext):
    id_security = call.data.split('_')[2]
    await state.update_data(sec_id=id_security)
    await call.message.answer(
        'Введите новый пароль', reply_markup=cancel_security_ikb
    )
    await Change.password.set()


@dp.message_handler(content_types=['text'], state=Change.login)
async def login_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    security_id = data['sec_id']
    user_security = (
        db.query(Employee).filter(Employee.id == security_id).first()
    )
    user_security.login = message.text
    db.commit()
    await message.answer('Логин успешно изменён')


@dp.message_handler(content_types=['text'], state=Change.password)
async def login_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    security_id = data['sec_id']
    user_security = (
        db.query(Employee).filter(Employee.id == security_id).first()
    )
    user_security.set_password(message.text)
    db.commit()
    await message.answer('Пароль успешно изменён')
