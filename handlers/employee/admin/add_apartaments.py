from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import start_admin_kb
from keyboards.inlines import cancel_add_ikb
from loader import dp, db
from models import Appartament, Employee
from states import Add, check

__all__ = []


@dp.callback_query_handler(text='cancel_add', state=Add,)
async def cancel_register_resident(
        call: types.CallbackQuery, state: FSMContext
):
    await state.finish()
    await call.message.answer('Отменено', reply_markup=start_admin_kb)


@dp.message_handler(text='Добавить квартиры')
async def add_apartaments(message: types.Message):
    admin = (
        db.query(Employee,)
        .filter(
            Employee.tg_user_id == message.from_user.id, Employee.is_admin == 1
        )
        .first()
    )
    if admin is not None:
        await message.answer(
            'Введите номер подъезда', reply_markup=cancel_add_ikb
        )
        await Add.padik.set()


@dp.message_handler(content_types=['text'], state=Add.padik)
async def set_apartaments(message: types.Message, state: FSMContext):
    padik = message.text
    if padik.isdigit():
        await state.update_data(padik=padik)
        await message.answer(
            'Введите номера квартир через "-" (пример 7-49)',
            reply_markup=cancel_add_ikb,
        )
        await Add.apartaments.set()
    else:
        await message.answer(
            'Подъезд должен быть числом', reply_markup=cancel_add_ikb
        )


@dp.message_handler(content_types=['text'], state=Add.apartaments)
async def set_apartaments(message: types.Message, state: FSMContext):
    apartaments_numbers = message.text
    status, error = check(apartaments_numbers)
    if status:
        already_exists = []
        one_number, two_number = error
        numbers = [i for i in range(int(one_number), int(two_number) + 1)]
        data = await state.get_data()
        padik = data['padik']
        for i in numbers:
            apartament = (
                db.query(Appartament)
                .filter(Appartament.number_appartament == i)
                .first()
            )
            if apartament is not None:
                already_exists.append(
                    f'Квартира с №{i} в подъезде {apartament.padik} уже зарегистрирована'
                )
            else:
                apartament = Appartament()
                apartament.padik = padik
                apartament.number_appartament = i
                db.add(apartament)
        db.commit()
        await state.finish()
        if len(already_exists) != 0:
            await message.answer(
                '\n'.join(already_exists)
                + '\n\nВсе квартиры зарегистрированы✅'
            )
        else:
            await message.answer('Все квартиры зарегистрированы✅')
    else:
        await message.answer(error, reply_markup=cancel_add_ikb)
