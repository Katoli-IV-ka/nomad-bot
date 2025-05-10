from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext


from handlers.booking.date.to_select_date import to_select_date
from utils.get_booked_dates import get_booking_dates

router = Router()


@router.callback_query(F.data == "booking")
async def booking_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    booked_dates = await get_booking_dates()
    await state.update_data(booked_dates=booked_dates)

    await to_select_date(state, callback)

