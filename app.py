from aiogram.contrib.middlewares.logging import LoggingMiddleware

__all__ = []


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from loader import Base, engine
    import models

    Base.metadata.create_all(engine)

    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
