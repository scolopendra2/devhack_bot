from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import cancel_resident_ikb
from keyboards import start_resident_kb
from loader import dp, db
from models import Resident, Appartament, Parking
from states import Register, RegisterResident


@dp.callback_query_handler(text='cancel_resident', state=RegisterResident)
async def cancel_register_resident(
    call: types.CallbackQuery, state: FSMContext
):
    await state.finish()
    await call.message.answer('Регистрация успешна прервана')
    await Register.register.set()


@dp.callback_query_handler(text='register_resident', state=Register.register)
async def register_resident(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == call.message.from_user.id)
        .first()
    )
    if resident is not None:
        await call.message.answer('Вы уже вошли в аккаунт')
    else:
        await call.message.answer(
            'Давайте начнем с вашего ФИО. Пожалуйста, '
            'введите ваше полное имя, фамилию и отчество через пробел.',
            reply_markup=cancel_resident_ikb,
        )
        await RegisterResident.fio.set()


@dp.message_handler(content_types=['text'], state=RegisterResident.fio)
async def set_fio(message: types.Message, state: FSMContext):
    split_message = message.text.split()
    if len(split_message) != 3:
        await message.answer(
            'Введите своё настоящее ФИО', reply_markup=cancel_resident_ikb
        )
    else:
        await state.update_data(fio=split_message)
        await message.answer(
            'Теперь пожалуйста пришлите мне свой номер телефона',
            reply_markup=cancel_resident_ikb,
        )
        await RegisterResident.phone_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterResident.phone_number
)
async def set_phone_number(message: types.Message, state: FSMContext):
    symbols = list(message.text)
    if len(list(filter(lambda x: x.isdigit(), symbols))) != 11:
        await message.answer(
            'Введите свой настоящий номер телефона',
            reply_markup=cancel_resident_ikb,
        )
    else:
        await state.update_data(
            phone_number=' '.join(list(map(lambda x: x.strip(), symbols)))
        )
        await message.answer(
            'Теперь пожалуйста пришлите мне номер своей квартиры',
            reply_markup=cancel_resident_ikb,
        )
        await RegisterResident.apartment_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterResident.apartment_number
)
async def apartment_number(message: types.Message, state: FSMContext):
    number_apartaments = message.text
    appartamentnts = db.query(Appartament).all()
    if number_apartaments not in list(
        map(lambda x: str(x.number_appartament), appartamentnts)
    ):
        await message.answer(
            'Квартиры нет в списке квартир дома попробуйте снова',
            reply_markup=cancel_resident_ikb,
        )
    else:
        await state.update_data(apartment_number=number_apartaments)
        await message.answer(
            'Теперь пожалуйста пришлите мне номер вашего парковочного места',
            reply_markup=cancel_resident_ikb,
        )
        await RegisterResident.parking_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterResident.parking_number
)
async def parking_number(message: types.Message, state: FSMContext):
    number_parking = message.text
    parking_place = db.query(Parking).all()
    if number_parking not in list(
        map(lambda x: str(x.number_place), parking_place)
    ):
        await message.answer(
            'Такого парковочного места не существует попробуйте снова',
            reply_markup=cancel_resident_ikb,
        )
    else:
        data = await state.get_data()
        surname, name, patronymic = data['fio']
        resident = Resident()
        resident.name = name
        resident.surname = surname
        resident.patronymic = patronymic
        resident.parking_id = (
            db.query(Parking)
            .filter(Parking.number_place == number_parking)
            .first()
            .id
        )
        resident.phone_number = data['phone_number']
        resident.apartment_id = (
            db.query(Appartament)
            .filter(Appartament.number_appartament == data['apartment_number'])
            .first()
            .id
        )
        resident.tg_user_id = message.from_user.id
        try:
            db.add(resident)
            db.commit()
        except Exception as ex:
            print(ex)
        await state.finish()
        await message.answer(
            'Вы успешно зарегистрировались', reply_markup=start_resident_kb
        )
