from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from contents.booking.keyboard_to_options import to_options_kb
from contents.booking.options_contents import get_options_text
from contents.booking.keyboard_share_contact import share_contact_keyboard
from states.booking_states import BookingState

router = Router()

@router.callback_query(F.data == "to_contact", BookingState.options_package_selection)
async def to_contact(state: FSMContext, callback: types.CallbackQuery = None):
    data = await state.get_data()
    package_options = data.get("package_options")
    process_message = data.get("process_message")

    # to_msg
    await process_message.edit_media(
        media = InputMediaPhoto(
            media = "AgACAgIAAxkBAAIBxWfrCu_-GGwWDFMrS_SiRH3tIY0TAAKs9TEb4TZZS3mMFih9kwuEAQADAgADcwADNgQ",
            caption = get_options_text(package_options),
        ),
        reply_markup = await to_options_kb()
    )

    # to_msg
    temp_message = await process_message.answer(
        text = "Пожалуйста, поделитесь своим номером телефона:",
        reply_markup=share_contact_keyboard()
    )

    await state.update_data(temp_message=temp_message)
    await state.set_state(BookingState.share_contact)