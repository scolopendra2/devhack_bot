from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import cancel_add_ikb
from loader import dp, db
from states import Add, check
from models import Parking, Employee


@dp.message_handler(text='Добавить парковочные места')
async def add_parking(message: types.Message):
    admin = (
        db.query(Employee)
        .filter(
            Employee.tg_user_id == message.from_user.id, Employee.is_admin == 1
        )
        .first()
    )
    if admin is not None:
        await message.answer(
            'Введите номерa парковочных мест "-" (пример 7-49)',
            reply_markup=cancel_add_ikb,
        )
        await Add.parkings.set()


@dp.message_handler(content_types=['text'], state=Add.parkings)
async def set_parking(message: types.message, state: FSMContext):
    parkings_numbers = message.text
    status, error = check(parkings_numbers)
    if status:
        already_exists = []
        one_number, two_number = error
        numbers = [i for i in range(int(one_number), int(two_number) + 1)]
        for i in numbers:
            parking = (
                db.query(Parking).filter(Parking.number_place == i).first()
            )
            if parking is not None:
                already_exists.append(
                    f'Парковочное место с №{i} уже зарегистрировано'
                )
            else:
                parking = Parking()
                parking.number_place = i
                db.add(parking)
        db.commit()
        await state.finish()
        if len(already_exists) != 0:
            await message.answer(
                '\n'.join(already_exists)
                + '\n\nВсе парковочные места зарегистрированы✅'
            )
        else:
            await message.answer('Все парковочные места зарегистрированы✅')
    else:
        await message.answer(error, reply_markup=cancel_add_ikb)
