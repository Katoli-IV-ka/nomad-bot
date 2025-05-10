from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from contents.delete_message_kb import delete_message_kb
from contents.menu.our_contacts_contents import our_contacts_text, our_contacts_photo

router = Router()

@router.callback_query(F.data == "our_contacts")
async def start_booking(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer_photo(
        photo = our_contacts_photo,
        caption = our_contacts_text,
        reply_markup=delete_message_kb()
    )

