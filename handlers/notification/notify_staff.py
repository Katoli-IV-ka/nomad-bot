from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import STAFF_TELEGRAM_ID
from contents.notification.staff_notification_contents import staff_notification_text
from handlers.notification.utils import get_tomorrow_bookings, get_ending_bookings
from main import bot as _bot

router = Router()

@router.message(Command("remind_staff"))
async def notify_staff(message: Message = None, bot: Bot = _bot):
    tomorrow_starts_bookings = get_tomorrow_bookings()
    if tomorrow_starts_bookings:
        await bot.send_message(
            chat_id=STAFF_TELEGRAM_ID,
            text=await staff_notification_text(tomorrow_starts_bookings[0]),
            parse_mode="HTML",
        )
    else:
        tomorrow_ending_bookings = get_ending_bookings()
        if tomorrow_ending_bookings:
            await bot.send_message(
                chat_id=STAFF_TELEGRAM_ID,
                text=await staff_notification_text(before_booking=True),
                parse_mode="HTML",
            )

    if message:
        await message.delete()



