from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards.menu_kb import main_menu_keyboard
from keyboards.options_package_kb import options_package_keyboard
from states.booking_states import BookingState

router = Router()

@router.callback_query(F.data == "back_to_options")
async def back_to_options_package(callback:CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.options_package_selection)

    await state.update_data(
        package_options = {
            "one_person": False,
            "two_person": False,
            "child": False,
            "pet": False,
            "koupel": False,
        }
    )

    # to_msg
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media="AgACAgIAAxkBAAIBw2frCujhFPLA8Xe2f_hL-ntRO2nJAAKr9TEb4TZZSy0fEuO6tM0qAQADAgADcwADNgQ",
            caption="Выберите условия проживания:",
            parse_mode="Markdown",
        ),
        reply_markup=options_package_keyboard({})
    )

    data = await state.get_data()
    req_contact_msg = data.get("req_contact_msg", None)

    if req_contact_msg:
        await req_contact_msg.delete()
        await state.update_data(req_contact_msg=None)