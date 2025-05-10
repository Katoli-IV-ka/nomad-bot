from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from contents.notification.client_notification_contents import client_notification_text
from handlers.notification.utils import get_tomorrow_bookings
from main import bot as _bot

router = Router()

@router.message(Command("remind_clients"))
async def notify_client(message: Message = None, bot: Bot = _bot):

    for booking_data in get_tomorrow_bookings():
        await bot.send_message(
            chat_id=int(booking_data["id"]),
            text=client_notification_text(booking_data),
            parse_mode="HTML",
        )

    if message:
        await message.delete()