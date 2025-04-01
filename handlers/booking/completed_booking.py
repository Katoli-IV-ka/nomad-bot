from aiogram import types, F, Router

from keyboards.menu_kb import menu_keyboard

router = Router()


@router.callback_query(F.data == "request_cash_payment")
async def confirm_cash_payment(callback: types.CallbackQuery):
    # to_msg
    await callback.message.answer_photo(
        photo = "AgACAgIAAxkBAAIDzmftvRL4l2yr7zER56n_K2RTOTPEAAK76TEbEqFwSxRGpZbJobEnAQADAgADcwADNgQ",
        caption= "Отлично, бронирование завершенно!"
                "Наш менеджер свяжется с вами для уточнения деталей\n"
                 "\n"
                 "А пока, пожалуйста уделите миниту чтоб прочитать наши правила, спасибо",
        reply_markup = menu_keyboard(),
    )

    await callback.message.reply_to_message.delete()
    await callback.message.delete()

