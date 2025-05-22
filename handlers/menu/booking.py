from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.booking.date.to_select_date import to_select_date
from utils.get_booked_dates import get_booking_dates

router = Router()

@router.message(Command('booking'))
async def wrapper(message: Message, state: FSMContext):
    await booking_callback(message=message,  state=state)

@router.callback_query(F.data == "booking")
async def booking_callback(callback: types.CallbackQuery = None, message: Message = None, state: FSMContext = None):
    await state.clear()

    if callback:
        message = callback.message

    booked_dates = await get_booking_dates()
    await state.update_data(booked_dates=booked_dates)

    await to_select_date(message=message, state=state, callback=None)

@router.callback_query(F.data == "back_to_booking")
async def booking_callback(callback: types.CallbackQuery = None,  state: FSMContext = None):
    await state.clear()

    booked_dates = await get_booking_dates()
    await state.update_data(booked_dates=booked_dates)

    await to_select_date(state=state, callback=callback)