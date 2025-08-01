from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from contents.booking.options_contents import get_options_text, to_options_kb
from contents.booking.share_contact_contents import share_contact_keyboard, share_contact_photo, request_contact_text
from states import BookingState

router = Router()

@router.callback_query(F.data == "to_contact", BookingState.options_package_selection)
async def to_contact(state: FSMContext, callback: types.CallbackQuery = None):
    data = await state.get_data()
    package_options = data.get("package_options")
    process_message = data.get("process_message")

    await process_message.edit_media(
        media = InputMediaPhoto(
            media = share_contact_photo,
            caption = get_options_text(package_options),
            parse_mode='HTML'
        ),
        reply_markup = await to_options_kb(),

    )

    # to_msg
    temp_message = await process_message.answer(
        text = request_contact_text,
        reply_markup=share_contact_keyboard()
    )

    await state.update_data(temp_message=temp_message)
    await state.set_state(BookingState.share_contact)