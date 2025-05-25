from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.booking.sammary.to_summary import to_summary
from states import BookingState


router = Router()

@router.message(BookingState.share_contact, F.contact)
async def receive_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    temp_message = data.get('temp_message', None)

    contact = message.contact
    username = message.from_user.username

    phone_number = contact.phone_number
    if phone_number and not phone_number.startswith("+"):
        phone_number = "+" + contact.phone_number

    await state.update_data(
        phone_number=phone_number,
        contact_name=contact.first_name + (" " + message.from_user.last_name if message.from_user.last_name else ""),
        telegram_user_id=contact.user_id,
        username=username
    )

    if temp_message:
        await temp_message.delete()
    await message.delete()

    await to_summary(state=state)
