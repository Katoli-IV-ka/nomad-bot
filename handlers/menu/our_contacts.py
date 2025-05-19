from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from contents.delete_message_kb import delete_message_kb
from contents.menu.our_contacts_contents import our_contacts_text, our_contacts_photo

router = Router()

@router.message(Command('contact'))
async def wrapper(message: Message = None, state: FSMContext = None):
    await start_booking(message=message,  state=state)

@router.callback_query(F.data == "our_contacts")
async def start_booking(callback: types.CallbackQuery = None, message: Message = None, state: FSMContext = None):
    if callback:
        message = callback.message

    await state.clear()

    await message.answer_photo(
        photo = our_contacts_photo,
        caption = our_contacts_text,
        reply_markup=delete_message_kb(text="Назад"),
        parse_mode='HTML'
    )

