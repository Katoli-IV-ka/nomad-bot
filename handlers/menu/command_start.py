from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from contents.menu.menu_contents import menu_photo, menu_keyboard, menu_text

router = Router()

@router.message(Command('start'))
async def admin_get_message_cmd(message: Message):
    await message.answer_photo(
        photo="AgACAgIAAxkBAAIJU2gZ3qn1RNP3mjWSHT3lBGRnTLT3AAKQ8DEbskjQSFj--ZUbev9BAQADAgADcwADNgQ",
        caption=menu_text,
        reply_markup=menu_keyboard(),
        parse_mode="HTML",
    )