from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import start_ikb, cancel_enter_ikb
from keyboards import start_admin_kb, start_security_kb
from loader import dp, db
from models import Employee
from states import EnterEmployee
from states import Register


@dp.callback_query_handler(text='cancel_enter', state=EnterEmployee)
async def cancel_register_resident(
    call: types.CallbackQuery, state: FSMContext
):
    await state.finish()
    await call.message.answer('Вход успешно прерван', reply_markup=start_ikb)
    await Register.register.set()


@dp.callback_query_handler(text='enter_employee', state=Register.register)
async def enter_employee(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Введите логин', reply_markup=cancel_enter_ikb)
    await EnterEmployee.login.set()


@dp.message_handler(content_types=['text'], state=EnterEmployee.login)
async def employee_login(message: types.Message, state: FSMContext):
    login = message.text
    logins = list(map(lambda x: x.login, db.query(Employee).all()))
    if login not in logins:
        await message.answer(
            'Такого логина не существует попробуйте снова',
            reply_markup=cancel_enter_ikb,
        )
    else:
        await state.update_data(login=login)
        await message.answer('Введите пароль', reply_markup=cancel_enter_ikb)
        await EnterEmployee.password.set()


@dp.message_handler(content_types=['text'], state=EnterEmployee.password)
async def employee_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    login = data['login']
    employee = db.query(Employee).filter(Employee.login == login).first()
    employee.tg_user_id = message.from_user.id
    db.commit()
    if employee.check_password(message.text) and employee.is_admin:
        await message.answer(
            'Вход успешно выполнен вам доступен функционал админа',
            reply_markup=start_admin_kb,
        )
        await state.finish()
    elif employee.check_password(message.text):
        await message.answer(
            'Вход успешно выполнен вам доступен функционал охраны',
            reply_markup=start_security_kb,
        )
        await state.finish()
    else:
        await message.answer(
            'Неверный пароль попробуйте снова', reply_markup=cancel_enter_ikb
        )
