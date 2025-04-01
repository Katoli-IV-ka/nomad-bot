import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from keyboards.booking_kb import BOOKED_DATES, generate_calendar
from keyboards.options_package_kb import options_package_keyboard
from states.booking_states import BookingState
from utils.mark_booked import mark_booked

router = Router()

# Начало выбора дат
@router.message(F.text == "Бронирование")
async def start_booking(message: types.Message, state: FSMContext):
    today = datetime.date.today()
    await state.clear()

    # to_msg
    await message.answer_photo(
        photo = "AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ",
        caption = "Выберите дату заезда:",
        reply_markup=generate_calendar(today.year, today.month)
    )
    await state.set_state(BookingState.check_in)



@router.callback_query(F.data.startswith("select|"))
async def select_date(callback: types.CallbackQuery, state: FSMContext):
    from datetime import date, timedelta

    _, y, m, d = callback.data.split("|")
    selected = date(int(y), int(m), int(d))

    # Проверка: нельзя выбрать день, если он полностью занят
    status = BOOKED_DATES.get(selected)
    if status == "full":
        await callback.answer("⛔ Дата полностью забронирована!", show_alert=True)
        return

    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")

    # Первая отметка
    if not check_in and not check_out:
        await state.update_data(check_in=selected)
    # Вторая — определим порядок
    elif check_in and not check_out:
        d1, d2 = sorted([check_in, selected])
        # Проверка допустимости диапазона
        for i in range((d2 - d1).days + 1):
            day = d1 + timedelta(days=i)
            status = BOOKED_DATES.get(day)
            if day == d1 and status in ("pm", "full"):
                await callback.answer("⛔ Дата заезда недоступна", show_alert=True)
                return
            if day == d2 and status in ("am", "full"):
                await callback.answer("⛔ Дата выезда недоступна", show_alert=True)
                return
            if d1 < day < d2 and status == "full":
                await callback.answer("⛔ В выбранном диапазоне есть забронированные дни", show_alert=True)
                return

        await state.update_data(check_in=d1, check_out=d2)
    else:
        # Сброс выбора
        await state.update_data(check_in=selected, check_out=None)

    new_data = await state.get_data()
    markup = generate_calendar(
        year=selected.year,
        month=selected.month,
        check_in=new_data.get("check_in"),
        check_out=new_data.get("check_out")
    )
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("switch|"))
async def switch_month(callback: types.CallbackQuery, state: FSMContext):
    _, year, month = callback.data.split("|")
    year, month = int(year), int(month)
    data = await state.get_data()
    markup = generate_calendar(
        year, month,
        check_in=data.get("check_in"),
        check_out=data.get("check_out")
    )
    await callback.message.edit_reply_markup(reply_markup=markup)


@router.callback_query(F.data == "confirm")
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    from datetime import timedelta

    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")

    # to_msg
    if not check_in or not check_out:
        await callback.answer("Сначала выберите даты", show_alert=True)
        return

    # ✅ Обновляем BOOKED_DATES
    mark_booked(check_in, "pm")  # заезд вечером
    mark_booked(check_out, "am")  # выезд утром

    for i in range(1, (check_out - check_in).days):
        day = check_in + timedelta(days=i)
        BOOKED_DATES[day] = "full"

    await callback.message.answer(
        f"Бронирование подтверждено с {check_in} по {check_out}"
    )
    await callback.message.delete()


# Это уже choice options
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
    choice_options_msg = await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBw2frCujhFPLA8Xe2f_hL-ntRO2nJAAKr9TEb4TZZSy0fEuO6tM0qAQADAgADcwADNgQ",
        caption="Выберите условия проживания:",
        reply_markup=options_package_keyboard({})
    )

    await state.update_data(choice_options_msg=choice_options_msg)
