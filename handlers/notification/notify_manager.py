from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import MANAGER_TELEGRAM_ID
from contents.notification.manager_notification_contents import manager_notification_text
from handlers.notification.utils import get_prepayment_only
from main import bot as _bot

router = Router()

@router.message(Command("remind_manager"))
async def notify_manager(message: Message = None, bot: Bot = _bot):
    booking_data = get_prepayment_only()

    if booking_data:
        booking_data = booking_data[0]

        await bot.send_message(
            chat_id=MANAGER_TELEGRAM_ID,
            text=manager_notification_text(booking_data),
            parse_mode="HTML",
        )

    if message:
        await message.delete()