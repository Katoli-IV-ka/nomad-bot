from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from messages.user_msg import start_message

router = Router()

@router.message(Command('start'))
async def admin_get_message_cmd(message: Message):
    await message.answer_photo(
        **start_message
    )