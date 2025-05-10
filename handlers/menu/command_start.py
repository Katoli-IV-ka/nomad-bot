from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from contents.menu.menu_contents import menu_photo, menu_keyboard, menu_text

router = Router()

@router.message(Command('menu'))
async def wrapper(message: Message = None):
    await menu_cmd(message=message)

@router.message(Command('start'))
async def menu_cmd(message: Message):
    await message.answer_photo(
        photo=menu_photo,
        caption=menu_text,
        reply_markup=menu_keyboard(),
        parse_mode="HTML",
    )