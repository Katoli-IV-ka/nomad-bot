from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from keyboards.delete_message import delete_message_kb

router = Router()

@router.callback_query(F.data == "our_contacts")
async def start_booking(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    # to_msg
    await callback.message.answer_photo(
        photo = "AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ",
        caption = "Наши контакты: \n"
                  f"inst: {None} \n"
                  f"связь с менеджером: {None} \n",
        reply_markup=delete_message_kb()
    )

