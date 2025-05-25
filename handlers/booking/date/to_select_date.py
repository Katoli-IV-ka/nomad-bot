from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from contents.booking.input_date_contents import input_date_photo, input_date_text, input_date_keyboard
from states import BookingState

router = Router()

@router.callback_query(F.data.startswith("to_select_date"))
async def to_select_date(message: Message = None, callback: CallbackQuery = None, state: FSMContext = None):
    data = await state.get_data()
    booked_dates = data.get('booked_dates')

    if callback:
        message = callback.message

        process_message = await message.edit_media(
            media=InputMediaPhoto(
                media=input_date_photo,
                caption=input_date_text,
                parse_mode="HTML",
            ),
            reply_markup=input_date_keyboard(booked_dates),
        )
    else:
        process_message = await message.answer_photo(
            photo = input_date_photo,
            caption = input_date_text,
            reply_markup = input_date_keyboard(booked_dates),
            parse_mode = 'HTML',
        )

    await state.set_state(BookingState.check_in)
    await state.update_data(process_message=process_message)