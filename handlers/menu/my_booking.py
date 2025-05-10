from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.notion_connect import get_pages_by_user_id
from contents.delete_message_kb import delete_message_kb
from contents.menu.my_bookings_contetns import format_bookings_overview, my_bookings_photo, get_to_booking_keyboard

router = Router()

@router.message(Command('my'))
async def wrapper(message: Message = None, state: FSMContext = None):
    await my_bookings(message=message,  state=state)

@router.callback_query(F.data == "my_booking")
async def my_bookings(message: Message = None, callback: types.CallbackQuery = None):
    if callback:
        message = callback.message

    user_id = str(message.chat.id)

    user_bookings = get_pages_by_user_id(
        user_id=user_id,
        payment_methods = ["Paid by card", "Paid by cash", "Other"]
    )

    if user_bookings:
        # to_msg
        await message.answer_photo(
            photo=my_bookings_photo,
            caption=format_bookings_overview(user_bookings),
            reply_markup=delete_message_kb("Назад")
        )
    else:
        # to_msg
        await message.answer_photo(
            photo=my_bookings_photo,
            caption=f"У вас нет активных броней, хотите забронировать?",
            reply_markup=get_to_booking_keyboard()
        )

