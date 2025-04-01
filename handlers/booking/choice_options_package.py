from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMedia, InputMediaPhoto

from keyboards.back_to_options_kb import back_to_options_package_kb
from keyboards.options_package_kb import options_package_keyboard
from keyboards.share_contact_kb import share_contact_keyboard
from states.booking_states import BookingState

router = Router()

@router.callback_query(F.data.startswith("package_options|"))
async def package_options(callback: types.CallbackQuery, state: FSMContext):
    _, option, exclusive_flag = callback.data.split("|")
    exclusive = bool(int(exclusive_flag))

    data = await state.get_data()
    package = data.get("package_options", {})

    if option == "film":
        await state.set_state(BookingState.shooting_share_contact)

        # to_msg
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media = "AgACAgIAAxkBAAIBx2frCvjAWpJs91hL7eVhpYTffn0nAAKt9TEb4TZZS56xO9ubLxYIAQADAgADcwADNgQ",
                caption="🎬 *Расшифровать как работает бронирование для съёмок*\n\n"
                        "Если вы планируете использовать дом для фотосессии, съёмки рекламы, фильмов и т.п., "
                        "мы обработаем вашу заявку индивидуально.",
                parse_mode="Markdown",
            ),
            reply_markup=await back_to_options_package_kb(),
        )

        # to_msg
        req_contact_msg = await callback.message.answer(
            text="Пожалуйста, поделитесь своим номером телефона:",
            reply_markup=share_contact_keyboard()
        )

        await state.update_data(req_contact_msg=req_contact_msg)

        return

    if exclusive:
        # сбросить все опции из той же группы
        if option == "one_person":
            package["one_person"] = True
            package["two_person"] = False
        elif option == "two_person":
            package["one_person"] = False
            package["two_person"] = True
    else:
        package[option] = not package.get(option, False)

    await state.update_data(package_options=package)

    try:
        await callback.message.edit_reply_markup(reply_markup=options_package_keyboard(package))
    except TelegramBadRequest:
        return



@router.callback_query(F.data == "continue_booking", BookingState.options_package_selection)
async def finish_package_selection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # to_msg
    package = data.get("package_options", {})
    text = "Вы выбрали:\n"

    mapping = {
        "one_person": "👤 Для одного",
        "two_person": "👥 Для двоих",
        "child": "🧒 С ребёнком",
        "pet": "🐶 С питомцем",
        "koupel": "🛁 Купель",
    }

    for key, label in mapping.items():
        if package.get(key):
            text += f"• {label}\n"




    # to_msg
    await callback.message.edit_media(
        media = InputMediaPhoto(
            media = "AgACAgIAAxkBAAIBxWfrCu_-GGwWDFMrS_SiRH3tIY0TAAKs9TEb4TZZS3mMFih9kwuEAQADAgADcwADNgQ",
            caption = f"{text}",
        ),
        reply_markup = await back_to_options_package_kb()
    )

    await callback.message.answer(
        text = "Пожалуйста, поделитесь своим номером телефона:",
        reply_markup=share_contact_keyboard()
    )

    await state.set_state(BookingState.share_contact)
