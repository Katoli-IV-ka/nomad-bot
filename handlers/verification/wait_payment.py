from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from contents.verification.payment_confirm_contetnts import confirm_payment_keyboard
from database.notion_connect import update_verification_by_page_id, check_payment_status, \
    update_payment_method_by_page_id
from handlers.verification.utils import check_payment
from schedule import scheduler

router = Router()

@router.callback_query(F.data.startswith("wait_payment"))
async def wait_payment(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_verification_by_page_id(
        page_id=notion_page_id,
        new_status="Waiting payment"
    )


    await callback.answer("💳 Бронирование ожидает оплаты")

    await callback.message.edit_caption(
        reply_markup = confirm_payment_keyboard(notion_page_id),
        caption = f"{callback.message.caption} \n"
                  f"\n"
                  f"💳 Бронирование ожидает оплаты, администратор: {'@'+callback.from_user.username if callback.from_user.username else callback.from_user.first_name}"
    )

    scheduler.add_job(
        check_payment,
        trigger='date',
        run_date=datetime.now() + timedelta(minutes=60),
        args = [notion_page_id],
    )