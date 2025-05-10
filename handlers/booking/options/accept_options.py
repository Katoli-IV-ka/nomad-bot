from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.booking.contact.to_contact import to_contact
from states.booking_states import BookingState

router = Router()


@router.callback_query(F.data == "accept_options", BookingState.options_package_selection)
async def accept_options(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    package_options = data.get("package_options")
    if not package_options['one_person'] and not package_options['two_person']:
        await callback.answer("Укажите количество гостей")
        return

    await to_contact(state=state)