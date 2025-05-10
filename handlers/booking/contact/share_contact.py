from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.booking.sammary.to_summary import to_summary
from states.booking_states import BookingState


router = Router()

@router.message(BookingState.share_contact, F.contact)
async def receive_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    username = message.from_user.username

    await state.update_data(
        phone_number=contact.phone_number,
        contact_name=contact.first_name + (" " + message.from_user.last_name if message.from_user.last_name else ""),
        telegram_user_id=contact.user_id,
        username=username
    )

    if message.reply_to_message:
        await message.reply_to_message.delete()
    await message.delete()

    await to_summary(state=state)
