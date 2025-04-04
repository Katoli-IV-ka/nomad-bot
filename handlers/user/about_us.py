from aiogram import Router, F

from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards.about_us_kb import about_us_kb

router = Router()
photo_index = 0
moon_phase_index = 0


@router.callback_query(F.data == "about_us")
async def on_callback_query(callback: CallbackQuery):
    global photo_index, moon_phase_index

    photo_index = 0
    moon_phase_index = 0

    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIE0WfuYMW5pJ20R350bRorXUKqwhB-AALH7TEbx1xwS-V8HcyauMHIAQADAgADcwADNgQ",
        reply_markup= await about_us_kb()
    )

@router.callback_query(F.data.startswith('photo_right'))
@router.callback_query(F.data.startswith('moon'))
@router.callback_query(F.data.startswith('photo_left'))
async def on_callback_query(callback: CallbackQuery):
    global photo_index, moon_phase_index

    # to_msg
    photos = [
        "AgACAgIAAxkBAAIE0WfuYMW5pJ20R350bRorXUKqwhB-AALH7TEbx1xwS-V8HcyauMHIAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE1GfuYOiJ2hx1hw3PlMc0cg1A96YKAALJ7TEbx1xwS1OP0ttivFybAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE1mfuYS5K1p7VrlRY_War9YHOhAEkAALK7TEbx1xwSxpbNWjKt4PiAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE2GfuYVayvWocZMewtFRLi_evJcOpAALM7TEbx1xwS6y2GI71c-iVAQADAgADcwADNgQ"
    ]

    # Эмодзи Луны
    moon_phases = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔"]

    data = callback.data

    # Обработка переключения фото
    if data.startswith("photo_left"):
        photo_index = (photo_index - 1) % len(photos)  # Циклический сдвиг по фотографиям
    elif data.startswith("photo_right"):
        photo_index = (photo_index + 1) % len(photos)  # Циклический сдвиг по фотографиям

    # Обработка переключения фазы луны
    elif data.startswith("moon"):
        moon_phase_index = (moon_phase_index + 1) % len(moon_phases)  # Циклический сдвиг по фазам луны

    # Обновление сообщения
    await callback.message.edit_media(
        media = InputMediaPhoto(media=photos[photo_index]),
        caption=f"Фото {photo_index + 1}/{len(photos)}",
        reply_markup=await about_us_kb(photo_index=photo_index, moon_phase_index=moon_phase_index)
    )

