from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.booking_states import BookingState

router = Router()

@router.callback_query(F.data == "delete_message")
async def delete_message(callback:CallbackQuery):

    # to_msg
    await callback.message.delete()

