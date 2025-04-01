from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from keyboards.menu_kb import main_menu_keyboard

router = Router()

@router.callback_query(F.data == "cancel_booking")
async def handle_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text="❌ Бронирование отменено.\nВы вернулись в главное меню.",
        reply_markup= main_menu_keyboard()
    )
    await callback.message.delete()