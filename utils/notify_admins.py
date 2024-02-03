from aiogram import Dispatcher

__all__ = []


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(chat_id=981197616, text='Bot Started')
