from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from contents.notification.client_notification_contents import client_notification_text, client_koupel_notification_text
from database.notion_connect import update_status_by_uniq_id
from handlers.notification.utils import get_tomorrow_bookings
from main import bot as _bot

router = Router()

@router.message(Command("remind_clients"))
async def notify_client(message: Message = None, bot: Bot = _bot):
    booking_data = get_tomorrow_bookings()

    if booking_data:
        booking_data = booking_data[0]


        await bot.send_message(
            chat_id=int(booking_data["id"]),
            text=client_notification_text(booking_data),
            parse_mode="HTML",
        )

        if bool(booking_data['koupel']) is True:
            await bot.send_message(
                chat_id=int(booking_data["id"]),
                text=client_koupel_notification_text,
                parse_mode="HTML",
            )

        update_status_by_uniq_id(
            uniq_id = booking_data["uniq_id"],
            new_status="Up-to-date booking"
        )

    if message:
        await message.delete()