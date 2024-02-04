import re
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import start_resident_kb
from keyboards.inlines import (
    all_access_ikb,
    cancel_all_access_ikb,
    delete_all_ikb,
    guest_access_ikb,
    cancel_guest_access_ikb,
    alive_ikb,
    delete_guesst_ikb,
)
from loader import dp, db, bot
from models import Car, Resident, Employee
from states import AddDeleteCars, AddDeleteCarsGuest


@dp.callback_query_handler(
    text='guest_access_cancel', state=AddDeleteCarsGuest
)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено', reply_markup=start_resident_kb)


@dp.callback_query_handler(text='all_access_cancel', state=AddDeleteCars)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено', reply_markup=start_resident_kb)


@dp.message_handler(text='Постоянный доступ')
async def all_access(message: types.Message):
    await message.answer('Выберите действие', reply_markup=all_access_ikb)


@dp.callback_query_handler(text='car_add')
async def add_car(call: types.CallbackQuery):
    await call.message.answer(
        'Введите номер машины\n пример <pre>в933хо 161</pre>',
        reply_markup=cancel_all_access_ikb,
    )
    await AddDeleteCars.number_car.set()


def validate_russian_license_plate(license_plate):
    pattern = re.compile(
        r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2} \d{2,3}$', re.IGNORECASE
    )

    if re.match(pattern, license_plate):
        return True
    else:
        return False


@dp.message_handler(content_types=['text'], state=AddDeleteCars.number_car)
async def number(message: types.Message, state: FSMContext):
    num_auto = message.text.upper()
    if validate_russian_license_plate(num_auto):
        await state.finish()
        resident = (
            db.query(Resident)
            .filter(Resident.tg_user_id == message.from_user.id)
            .first()
        )
        car = Car()
        car.gos_number = num_auto.lower()
        car.resident_id = resident.id
        db.add(car)
        db.commit()
        await message.answer(
            'Машина успешно добавлена в постоянные доступ',
            reply_markup=start_resident_kb,
        )
    else:
        await message.answer(
            'Гос номер не соотевтствует стандарту попробуйте ещё раз',
            reply_markup=cancel_all_access_ikb,
        )


@dp.callback_query_handler(text='car_delete')
async def car_delete(call: types.CallbackQuery):
    ikb = delete_all_ikb(call.from_user.id)
    await call.message.answer(
        'Выберите машину которую хотите удалить', reply_markup=ikb
    )


@dp.callback_query_handler(lambda x: x.data.startswith('cardelete_'))
async def delete_car(call: types.CallbackQuery):
    id_car = call.data.split('_')[1]
    car = db.query(Car).filter(Car.id == id_car).first()
    try:
        db.delete(car)
        db.commit()
    except Exception:
        pass
    await call.message.answer(
        'Машина успешно удалена', reply_markup=start_resident_kb
    )


@dp.callback_query_handler(text='car_list')
async def list_car(call: types.CallbackQuery):
    tg_user_id = call.from_user.id
    resident = (
        db.query(Resident).filter(Resident.tg_user_id == tg_user_id).first()
    )
    numbers = (
        db.query(Car)
        .filter(Car.resident_id == resident.id, Car.date_end == None)
        .all()
    )
    cars = ['Номер авто/Дата регистрации\n']
    for num in numbers:
        cars.append(f'<pre>{num.gos_number}</pre> {num.date_start}')
    if len(cars) == 1:
        await call.message.answer('У вас нет машин')
    else:
        await call.message.answer('\n'.join(cars))


@dp.message_handler(text='Гостевой доступ')
async def all_access(message: types.Message):
    await message.answer('Выберите действие', reply_markup=guest_access_ikb)


@dp.callback_query_handler(text='guest_car_add')
async def guest_car_add(call: types.CallbackQuery):
    await call.message.answer(
        'Введите номер машины\n пример <pre>в933хо 161</pre>',
        reply_markup=cancel_guest_access_ikb,
    )
    await AddDeleteCarsGuest.number_car.set()


@dp.message_handler(
    content_types=['text'], state=AddDeleteCarsGuest.number_car
)
async def number(message: types.Message, state: FSMContext):
    num_auto = message.text.upper()
    if validate_russian_license_plate(num_auto):
        await state.update_data(number_car=num_auto.lower())
        await message.answer('Выберите время действия', reply_markup=alive_ikb)
        await AddDeleteCarsGuest.alive.set()
    else:
        await message.answer(
            'Гос номер не соотевтствует стандарту попробуйте ещё раз',
            reply_markup=cancel_guest_access_ikb,
        )


@dp.callback_query_handler(
    lambda x: x.data.startswith('hour_'), state=AddDeleteCarsGuest.alive
)
async def alive(call: types.CallbackQuery, state: FSMContext):
    hour = int(call.data.split('_')[1])
    data = await state.get_data()
    await state.finish()
    date_end = datetime.now() + timedelta(hours=hour)
    gos = data['number_car']
    tg_user_id = call.from_user.id
    resident = (
        db.query(Resident).filter(Resident.tg_user_id == tg_user_id).first()
    )
    car = Car()
    car.gos_number = gos
    car.date_end = date_end
    car.resident_id = resident.id
    db.add(car)
    db.commit()
    employees = db.query(Employee).all()
    for employee in employees:
        try:
            await bot.send_message(
                chat_id=employee.tg_user_id,
                text=f'Пользователь {call.from_user.full_name}\n'
                f'Добавил машину с гос номером <pre>{gos}</pre>'
                f' в гостевой список',
            )
        except Exception as ex:
            pass
    await call.message.answer('Доступ к парковке открыт')


@dp.callback_query_handler(text='guest_car_delete')
async def guest_car_delete(call: types.CallbackQuery):
    ikb = delete_guesst_ikb(call.from_user.id)
    await call.message.answer(
        'Выберите машину которой нужно закрыть доступ к парковке',
        reply_markup=ikb,
    )


@dp.callback_query_handler(lambda x: x.data.startswith('guestdelete_'))
async def delete_car(call: types.CallbackQuery):
    id_car = call.data.split('_')[1]
    car = db.query(Car).filter(Car.id == id_car).first()
    try:
        db.delete(car)
        db.commit()
    except Exception:
        pass
    await call.message.answer(
        'Машина успешно удалена', reply_markup=start_resident_kb
    )


@dp.callback_query_handler(text='guest_car_list')
async def list_car(call: types.CallbackQuery):
    tg_user_id = call.from_user.id
    resident = (
        db.query(Resident).filter(Resident.tg_user_id == tg_user_id).first()
    )
    numbers = (
        db.query(Car)
        .filter(Car.resident_id == resident.id, Car.date_end != None)
        .all()
    )
    cars = ['Номер авто/Дата регистрации/Дата окончания\n']
    for num in numbers:
        cars.append(
            f'<pre>{num.gos_number}</pre> с {num.date_start} до {num.date_end}'
        )
    if len(cars) == 1:
        await call.message.answer('У вас нет машин')
    else:
        await call.message.answer('\n'.join(cars))
