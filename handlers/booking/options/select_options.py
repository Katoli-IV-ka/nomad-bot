from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from contents.booking.options_contents import get_options_keyboard


router = Router()

@router.callback_query(F.data.startswith("package_options"))
async def package_options(callback: types.CallbackQuery, state: FSMContext):
    _, option, exclusive_flag = callback.data.split("|")
    exclusive = bool(int(exclusive_flag))

    data = await state.get_data()
    package = data.get("package_options", {})

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
        await callback.message.edit_reply_markup(reply_markup=get_options_keyboard(package))
    except TelegramBadRequest:
        return




