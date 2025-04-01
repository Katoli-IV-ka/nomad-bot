from aiogram import types, F, Router

router = Router()

@router.callback_query(F.data == "pay_cash")
async def handle_cash_payment(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💵 *Оплата наличными*\n\n"
        "Вы можете оплатить наличными при заселении.\n"
        "Пожалуйста, предупредите администратора заранее и подготовьте сумму без сдачи.",
        parse_mode="Markdown"
    )