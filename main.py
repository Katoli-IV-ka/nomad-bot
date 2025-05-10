import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from config import BOT_TOKEN, DEV_TELEGRAM_USER_ID

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():

    # Регистрация обработчиков
    from loader import loader
    loader(dp)

    # Запуск планировщика
    from schedule import scheduler
    scheduler.start()

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)

    #трекинг бота
    await bot.send_message(
        chat_id=DEV_TELEGRAM_USER_ID,
        text="Bot is running..."
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



