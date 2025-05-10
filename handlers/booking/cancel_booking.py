from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "cancel_booking")
async def handle_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()