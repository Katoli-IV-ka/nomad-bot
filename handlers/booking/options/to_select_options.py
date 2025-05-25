from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from contents.booking.options_contents import get_options_keyboard, options_photo
from states import BookingState

router = Router()

@router.callback_query(F.data == "to_options")
async def to_select_options(callback:CallbackQuery = None, state: FSMContext = None):
    await state.set_state(BookingState.options_package_selection)

    data = await state.get_data()
    process_message = data.get('process_message')
    temp_message = data.get("temp_message")

    await process_message.edit_media(
        media=InputMediaPhoto(
            media=options_photo,
            caption="Выберите условия проживания:",
            parse_mode="HTML",
        ),
        reply_markup=get_options_keyboard({})
    )

    await state.update_data(
        package_options={
            "one_person": False,
            "two_person": False,
            "child": False,
            "pet": False,
            "koupel": False,
        }
    )

    try:
        await temp_message.delete()
        await state.update_data(temp_message=None)
    except Exception:
        pass