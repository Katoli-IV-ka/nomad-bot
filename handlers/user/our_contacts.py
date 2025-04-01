from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "Бронирование")
async def start_booking(message: types.Message, state: FSMContext):
    await state.clear()

    # to_msg
    await message.answer_photo(
        photo = "AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ",
        caption = "Выберите дату заезда:",
        reply_markup=generate_calendar()
    )
    await state.set_state(BookingState.check_in)
