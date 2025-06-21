from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from database.notion_connect import update_verification_by_page_id

router = Router()

@router.callback_query(F.data.startswith("reject_booking"))
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_verification_by_page_id(
        page_id=notion_page_id,
        new_status="Booking rejection"
    )

    await callback.answer("🚫 Бронирование отклонено")

    await callback.message.edit_caption(
        reply_markup = None,
        caption=f"<b>Статус</b>: 🚫 Бронирование отклонено\n"
                f"Администратор: {'@' + callback.from_user.username if callback.from_user.username else callback.from_user.first_name}\n"
                f"———\n"
                f"\n"
                f"{callback.message.caption}"
    )
