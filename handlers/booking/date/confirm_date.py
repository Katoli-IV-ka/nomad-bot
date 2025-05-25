from datetime import date

from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from contents.booking.input_date_contents import input_date_alerts
from handlers.booking.options.to_select_options import to_select_options
from states import BookingState


router = Router()



@router.callback_query(F.data == "confirm_date")
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")

    if not check_in:
        await callback.answer('📅 Сначала выберите дату ', show_alert=True)
        return
    elif not check_out:
        await state.update_data(check_out=check_in)

    today = date.today()

    if check_in:
        d_in = date.fromisoformat(str(check_in))
        if d_in <= today:
            await callback.answer('❌ Дата бронирования должна быть в будущем.', show_alert=True)
            return
    if check_out:
        d_out = date.fromisoformat(str(check_out))
        if d_out <= today:
            await callback.answer('❌ Дата бронирования должна быть в будущем.', show_alert=True)
            return


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
