from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from contents.menu.about_us_contents import about_us_kb, about_us_contents

router = Router()
photo_index = 0

@router.message(Command('nomad'))
async def wrapper(message: Message = None):
    await about_us(message=message)

@router.callback_query(F.data == "about_us")
async def about_us(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None):
    global photo_index

    if callback:
        message = callback.message

    photo_index = 0

    await message.answer_photo(
        photo=about_us_contents[0]['media'],
        caption=about_us_contents[0]['text'],
        reply_markup= await about_us_kb()
    )


@router.callback_query(F.data.startswith('photo_right'))
@router.callback_query(F.data.startswith('photo_left'))
async def on_callback_query(callback: CallbackQuery):
    global photo_index

    # to_msg
    data = callback.data

    # Обработка переключения фото
    if data.startswith("photo_left"):
        photo_index = (photo_index - 1) % len(about_us_contents)  # Циклический сдвиг по фотографиям
    elif data.startswith("photo_right"):
        photo_index = (photo_index + 1) % len(about_us_contents)  # Циклический сдвиг по фотографиям

    # Обновление сообщения
    await callback.message.edit_media(
        media = InputMediaPhoto(
            media=about_us_contents[photo_index]['media'],
            caption=about_us_contents[photo_index]['text'],
            parse_mode='HTML'
        ),
        reply_markup=await about_us_kb(photo_index=photo_index)
    )

