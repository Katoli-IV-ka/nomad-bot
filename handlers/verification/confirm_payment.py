from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from database.notion_connect import update_payment_method_by_page_id, update_verification_by_page_id

router = Router()

@router.callback_query(F.data.startswith("confirm_payment"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_payment_method_by_page_id(page_id=notion_page_id, new_method="By card")
    update_verification_by_page_id(page_id=notion_page_id, new_status="Waiting visit")

    await callback.answer("✅ Бронирование подтверждено")

    caption_without_last_two = "\n".join(callback.message.caption.splitlines()[:-2])

    await callback.message.edit_caption(
        reply_markup = None,
        caption = f"{caption_without_last_two} \n"
                  f"\n"
                  f"🏕 Бронирование подтверждено, администратор: {'@'+callback.from_user.username if callback.from_user.username else callback.from_user.first_name}"
                  f""
    )