from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database.notion_connect import get_pages_by_user_id
from keyboards.delete_message import delete_message_kb
from utils.format_booking_message import format_booking_message

router = Router()

@router.callback_query(F.data == "my_booking")
async def my_bookings(callback: types.CallbackQuery, state: FSMContext):

    user_bookings = get_pages_by_user_id(str(callback.message.chat.id))

    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ",
        caption="Список ваших бронирований:",
    )

    if user_bookings:
        for booking in user_bookings:

            # to_msg
            await callback.message.answer(
                text=format_booking_message(booking),
                reply_markup=delete_message_kb()
            )
    else:
        # to_msg
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ",
            caption=f"У вас нет активных броней, хотите забронировать?",
        )