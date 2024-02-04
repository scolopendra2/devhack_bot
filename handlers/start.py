from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import agree_ikb, start_ikb
from loader import dp, bot
from states import AgreeConf, Register

__all__ = []


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    file_path = 'personal_data_processing_agreement/FV_BIT_CONF.docx'
    with open(file_path, 'rb') as file:
        await bot.send_document(
            message.chat.id,
            types.InputFile(file),
            caption='Привет! 👋 Я твой персональный бот для управления доступом в жилом комплексе. '
            'Я помогу тебе отправлять запросы на открытие '
            'шлагбаума, управлять номерами парковочных мест, а '
            'также предоставлять информацию о постояльцах.\n\n'
            'Чтобы продолжить прими согласие на обработку персональных данных 🤖🏠',
            reply_markup=agree_ikb,
        )
    await AgreeConf.agree.set()


@dp.callback_query_handler(text='agree', state=AgreeConf.agree)
async def agree(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        'Спасибо за согласие! 🎉\nТеперь вы можете продолжить использование наших услуг.',
        reply_markup=start_ikb,
    )
    await state.finish()
    await Register.register.set()


@dp.message_handler(content_types=['text'], state=AgreeConf.agree)
async def not_agree(message: types.Message):
    await message.answer(
        'Для продолжения необходимо принять соглашение на обработку персональных данных'
    )


@dp.message_handler(content_types=['text'], state=Register.register)
async def not_agree(message: types.Message):
    await message.answer(
        'Для продолжения необходимо пройти регистрацию или войти в аккаунт(для сотрудников УК)',
        reply_markup=start_ikb,
    )
