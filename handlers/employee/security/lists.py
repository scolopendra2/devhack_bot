from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import start_security_kb
from keyboards.inlines import cancel_check_ikb
from loader import dp, db
from models import Car, Resident
from states import CheckGos


@dp.callback_query_handler(text='cancel_check_number', state=CheckGos)
async def check_gos_number(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено', reply_markup=start_security_kb)


@dp.message_handler(text='Список постоянных пропусков')
async def all_list(message: types.Message):
    messages = []
    residents = db.query(Resident).all()
    for resident in residents:
        start = f'{resident.surname} {resident.name}:\n\n'
        cars = (
            db.query(Car)
            .filter(Car.resident_id == resident.id, Car.date_end == None)
            .all()
        )
        for car in cars:
            start += f'<pre>{car.gos_number}</pre> {car.date_start}\n'
        messages.append(start)
    if len(messages) != 0:
        await message.answer('\n\n'.join(messages))
    else:
        await message.answer('Данные пусты')


@dp.message_handler(text='Список временных пропусков')
async def all_list(message: types.Message):
    messages = []
    residents = db.query(Resident).all()
    for resident in residents:
        start = f'{resident.surname} {resident.name}:\n\n'
        cars = (
            db.query(Car)
            .filter(Car.resident_id == resident.id, Car.date_end != None)
            .all()
        )
        for car in cars:
            start += f'<pre>{car.gos_number}</pre> с {car.date_start} до {car.date_end}\n'
        messages.append(start)
    if len(messages) != 0:
        await message.answer('\n\n'.join(messages))
    else:
        await message.answer('Данные пусты')


@dp.message_handler(text='Проверить номер')
async def check_number(message: types.Message):
    await message.answer(
        'Введите номер машины\n пример <pre>в933хо 161</pre>',
        reply_markup=cancel_check_ikb,
    )
    await CheckGos.gos.set()


@dp.message_handler(content_types=['text'], state=CheckGos.gos)
async def check(message: types.Message, state: FSMContext):
    gos = message.text
    car = db.query(Car).filter(Car.gos_number == gos).first()
    if car is None:
        await message.answer(
            'Машина не найдена в разрешённых', reply_markup=cancel_check_ikb
        )
    else:
        if car.date_end == None:
            await message.answer(
                f'Машина найдена в списке постояльцев\n'
                f'ФИО: {car.resident.surname} {car.resident.name} {car.resident.patronymic}\n'
                f'Дата создания: {car.date_start}',
                reply_markup=start_security_kb,
            )
        else:
            await message.answer(
                f'Машина найдена в списке гостей\n'
                f'ФИО кто дал доступ: {car.resident.surname} {car.resident.name} '
                f'{car.resident.patronymic}\n'
                f'Дата создания: {car.date_start}\n'
                f'Дата дейтсвия до: {car.date_end}',
                reply_markup=start_security_kb,
            )
        await state.finish()
