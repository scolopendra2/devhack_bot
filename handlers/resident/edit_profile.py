from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import edit_profile_ikb, cancel_edit_profile_ikb
from keyboards import start_resident_kb
from loader import dp, db
from models import Resident, Appartament, Parking
from states import EditProfile


@dp.callback_query_handler(text='cancel_edit_profile', state=EditProfile)
async def cancel_edit_profile(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Отменено')


@dp.message_handler(text='Редактировать профиль')
async def edit_profile(message: types.Message):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    if resident is not None:
        await message.answer(
            f'Ваши данные:\n\n'
            f'Фамилия: {resident.surname}\n'
            f'Имя: {resident.name}\n'
            f'Отчество: {resident.patronymic}\n'
            f'Номер телефона: {resident.phone_number}\n'
            f'Номер квартиры: {resident.appartament.number_appartament}\n'
            f'Номер парковочного места: {resident.parking.number_place}',
            reply_markup=edit_profile_ikb,
        )


@dp.callback_query_handler(text='surname_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новую фамилию', reply_markup=cancel_edit_profile_ikb
    )
    await EditProfile.surname.set()


@dp.message_handler(content_types=['text'], state=EditProfile.surname)
async def edit_surname(message: types.Message, state: FSMContext):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    resident.surname = message.text
    db.commit()
    await state.finish()
    await message.answer(
        'Фамилия успешно изменена', reply_markup=start_resident_kb
    )


@dp.callback_query_handler(text='name_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новое имя', reply_markup=cancel_edit_profile_ikb
    )
    await EditProfile.name.set()


@dp.message_handler(content_types=['text'], state=EditProfile.name)
async def edit_surname(message: types.Message, state: FSMContext):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    resident.name = message.text
    db.commit()
    await state.finish()
    await message.answer(
        'Имя успешно изменено', reply_markup=start_resident_kb
    )


@dp.callback_query_handler(text='patronymic_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новое отчество', reply_markup=cancel_edit_profile_ikb
    )
    await EditProfile.patronymic.set()


@dp.message_handler(content_types=['text'], state=EditProfile.patronymic)
async def edit_surname(message: types.Message, state: FSMContext):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    resident.patronymic = message.text
    db.commit()
    await state.finish()
    await message.answer(
        'Отчество успешно изменено', reply_markup=start_resident_kb
    )


@dp.callback_query_handler(text='phone_number_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новый номер телефона', reply_markup=cancel_edit_profile_ikb
    )
    await EditProfile.phone_number.set()


@dp.message_handler(content_types=['text'], state=EditProfile.phone_number)
async def edit_surname(message: types.Message, state: FSMContext):
    symbols = list(message.text)
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    if len(list(filter(lambda x: x.isdigit(), symbols))) != 11:
        await message.answer(
            'Введите свой настоящий номер телефона',
            reply_markup=cancel_edit_profile_ikb,
        )
    else:
        resident.phone_number = ' '.join(
            list(map(lambda x: x.strip(), list(message.text)))
        )
        db.commit()
        await state.finish()
        await message.answer(
            'Номер телефона успешно изменен', reply_markup=start_resident_kb
        )


@dp.callback_query_handler(text='number_appartament_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новый номер квартиры', reply_markup=cancel_edit_profile_ikb
    )
    await EditProfile.number_appartament.set()


@dp.message_handler(
    content_types=['text'], state=EditProfile.number_appartament
)
async def edit_surname(message: types.Message, state: FSMContext):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    number_apartaments = message.text
    appartamentnts = db.query(Appartament).all()
    if number_apartaments not in list(
        map(lambda x: str(x.number_appartament), appartamentnts)
    ):
        await message.answer(
            'Квартиры нет в списке квартир дома попробуйте снова',
            reply_markup=cancel_edit_profile_ikb,
        )
    else:
        resident.apartment_id = (
            db.query(Appartament)
            .filter(Appartament.number_appartament == number_apartaments)
            .first()
            .id
        )
        db.commit()
        await state.finish()
        await message.answer(
            'Номер квартиры успешно изменен', reply_markup=start_resident_kb
        )


@dp.callback_query_handler(text='number_place_edit')
async def surname(call: types.CallbackQuery):
    await call.message.answer(
        'Введите новый номер парковочного места',
        reply_markup=cancel_edit_profile_ikb,
    )
    await EditProfile.number_place.set()


@dp.message_handler(content_types=['text'], state=EditProfile.number_place)
async def edit_surname(message: types.Message, state: FSMContext):
    resident = (
        db.query(Resident)
        .filter(Resident.tg_user_id == message.from_user.id)
        .first()
    )
    number_parking = message.text
    parking_place = db.query(Parking).all()
    if number_parking not in list(
        map(lambda x: str(x.number_place), parking_place)
    ):
        await message.answer(
            'Такого парковочного места не существует попробуйте снова',
            reply_markup=cancel_edit_profile_ikb,
        )
    else:
        resident.parking_id = (
            db.query(Parking)
            .filter(Parking.number_place == int(number_parking))
            .first()
            .id
        )
        db.commit()
        await state.finish()
        await message.answer(
            'Номер парковочного места успешно изменен',
            reply_markup=start_resident_kb,
        )
