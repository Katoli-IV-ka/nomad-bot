from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.notion_connect import get_pages_by_user_id
from contents.delete_message_kb import delete_message_kb
from contents.menu.my_bookings_contetns import format_bookings_overview, my_bookings_photo, get_to_booking_keyboard, \
    my_bookings_empty_text

router = Router()

@router.message(Command('my'))
async def wrapper(message: Message = None):
    await my_bookings(message=message)

@router.callback_query(F.data == "my_booking")
async def my_bookings(callback: types.CallbackQuery = None, message: Message = None):
    if callback:
        message = callback.message

    user_id = str(message.chat.id)

    user_bookings = get_pages_by_user_id(
        user_id=user_id,
        allowed_status= ["Completed booking", "Up-to-date booking", "Waiting visit"]
    )

    if user_bookings:
        # to_msg
        await message.answer_photo(
            photo=my_bookings_photo,
            caption=format_bookings_overview(user_bookings),
            reply_markup=delete_message_kb("Назад"),
            parse_mode='HTML'
        )
    else:
        # to_msg
        await message.answer_photo(
            photo=my_bookings_photo,
            caption=my_bookings_empty_text,
            reply_markup=get_to_booking_keyboard(),
            parse_mode='HTML'
        )

