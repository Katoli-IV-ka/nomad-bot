from aiogram import types, F, Router

from keyboards.pay_cash_kb import pay_cash_kb

router = Router()

@router.callback_query(F.data == "pay_cash")
async def handle_cash_payment(callback: types.CallbackQuery):
    # to_msg
    await callback.message.reply(
        text= "Для оплаты наличными необходимо подтверждение бронирования\n" 
              "В ближайшее время с вами свяжется наш администратор для уточнения информации. " 
              "Так же вы можете получить моментальное бронирование оплатив онлайн\n",
        reply_markup=await pay_cash_kb(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "back_to_summary")
async def cancel_cash_payment(callback: types.CallbackQuery):
    await callback.message.delete()