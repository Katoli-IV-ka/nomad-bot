import logging
from pprint import pprint

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from main import bot

router = Router()

@router.message(Command('get'))
async def admin_get_message_cmd(message: Message):

    def format_message(data: dict) -> str:
        return "\n".join(
            f"<b>{key}</b>: {str(value)[:400]}..." if len(str(value)) > 400 else f"<b>{key}</b>: {value}"
            for key, value in data.items() if value is not None
        )

    def log_message_data(msg: Message, prefix: str):
        logging.info(f"\n🔹 {prefix} Message from {msg.from_user.id}:")
        pprint(msg.model_dump(), width=100, indent=2)

    log_message_data(message, "Получено")

    await bot.send_message(
        chat_id=message.from_user.id,
        text=format_message(message.model_dump()),
        parse_mode="HTML"
    )

    if message.reply_to_message:
        log_message_data(message.reply_to_message, "Ответ на сообщение")
        await bot.send_message(
            chat_id=message.from_user.id,
            text=format_message(message.reply_to_message.model_dump()),
            parse_mode="HTML"
        )