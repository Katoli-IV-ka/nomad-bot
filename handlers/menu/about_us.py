from aiogram import Router, F
from aiogram.filters import Command

from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from contents.menu.about_us_contents import about_us_kb, about_us_photos

router = Router()
photo_index = 0

@router.message(Command('nomad'))
@router.callback_query(F.data == "about_us")
async def on_callback_query(message: Message = None, callback: CallbackQuery = None):
    global photo_index
    if callback:
        message = callback.message

    photo_index = 0

    await message.answer_photo(
        photo=about_us_photos[0],
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
        photo_index = (photo_index - 1) % len(about_us_photos)  # Циклический сдвиг по фотографиям
    elif data.startswith("photo_right"):
        photo_index = (photo_index + 1) % len(about_us_photos)  # Циклический сдвиг по фотографиям

    # Обновление сообщения
    await callback.message.edit_media(
        media = InputMediaPhoto(media=about_us_photos[photo_index]),
        caption=f"Фото {photo_index + 1}/{len(about_us_photos)}",
        reply_markup=await about_us_kb(photo_index=photo_index)
    )

