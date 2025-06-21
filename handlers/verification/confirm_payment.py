from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from contents.verification.payment_confirm_contetnts import confirm_payment_keyboard
from database.notion_connect import update_verification_by_page_id
from schedule import scheduler

router = Router()

@router.callback_query(F.data.startswith("confirm_payment"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_verification_by_page_id(page_id=notion_page_id, new_status="Waiting visit")

    await callback.answer("✅ Бронирование подтверждено")

    caption_without_last_two = "\n".join(callback.message.caption.splitlines()[4:])

    await callback.message.edit_caption(
        reply_markup = None,
        caption = f"<b>Статус</b>: ✅ Внесена полная оплата\n"
                  f"Администратор: {'@'+callback.from_user.username if callback.from_user.username else callback.from_user.first_name}\n"
                  f"———\n"
                  f"\n"
                  f"{caption_without_last_two} \n",
        caption_entities=callback.message.caption_entities,
        parse_mode = "HTML"
    )


@router.callback_query(F.data.startswith("confirm_prepayment"))
async def confirm_prepayment(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_verification_by_page_id(page_id=notion_page_id, new_status="Prepayment received")

    await callback.answer("💳 Предоплата полученна")

    caption_without_last_two = "\n".join(callback.message.caption.splitlines()[4:])

    await callback.message.edit_caption(
        reply_markup = confirm_payment_keyboard(
            notion_page_id=notion_page_id,
            only_payment=True,
        ),
        caption = f"<b>Статус</b>: 💳 Внесена предоплата\n"
                  f"Администратор: {'@'+callback.from_user.username if callback.from_user.username else callback.from_user.first_name}\n"
                  f"———\n"
                  f"\n"
                  f"{caption_without_last_two} \n",
        caption_entities=callback.message.caption_entities,
        parse_mode = "HTML"
    )


@router.callback_query(F.data.startswith("cancel_payment"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    _, _, notion_page_id = callback.data.split("_")

    update_verification_by_page_id(page_id=notion_page_id, new_status="Cancel payment")

    await callback.answer("🚫 Оплата отменена")

    caption_without_last_two = "\n".join(callback.message.caption.splitlines()[4:])

    await callback.message.edit_caption(
        reply_markup = None,
        caption = f"<b>Статус</b>: 🚫 Оплата отменена\n"
                  f"Администратор: {'@'+callback.from_user.username if callback.from_user.username else callback.from_user.first_name}\n"
                  f"———\n"
                  f"\n"
                  f"{caption_without_last_two} \n",
        caption_entities=callback.message.caption_entities,
        parse_mode = "HTML"
    )