from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from contents.booking.input_date_contents import input_date_alerts
from handlers.booking.options.to_select_options import to_select_options
from states.booking_states import BookingState


router = Router()

@router.callback_query(F.data == "confirm_date")
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")

    await callback.answer(**input_date_alerts(check_in, check_out))
    if not check_in:
        return
    elif not check_out:
        await state.update_data(check_out=check_in)

    # Это уже choice options
    await state.set_state(BookingState.options_package_selection)
    await state.update_data(
        package_options = {
            "one_person": False,
            "two_person": False,
            "child": False,
            "pet": False,
            "koupel": False,
        }
    )

    await to_select_options(state=state)
