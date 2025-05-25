from datetime import date, timedelta
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from contents.booking.input_date_contents import input_date_keyboard

router = Router()

@router.callback_query(F.data == "noop")
async def confirm_booking(callback: types.CallbackQuery):
    await callback.answer('🚫 Дата недоступна', show_alert=True)


@router.callback_query(F.data.startswith("select"))
async def select_date(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    check_in = data.get("check_in")      # date or None
    check_out = data.get("check_out")    # date or None
    booked = set(data.get("booked_dates", []))

    # Распарсим callback.data: "select|YYYY|MM|DD"
    _, y, m, d = callback.data.split("|")
    selected = date(int(y), int(m), int(d))


    if check_in and not check_out and selected == check_in:
        await state.update_data(check_in=None, check_out=None)
    elif check_in and check_out and selected in {check_in, check_out}:
        await state.update_data(check_in=None, check_out=None)
    else:
        if check_in is None and check_out is None:
            await state.update_data(check_in=selected)

        # Если есть только check_in — ставим check_out (сортируя границы)
        elif check_in is not None and check_out is None:
            start, end = sorted([check_in, selected])
            # Проверяем занятые даты в диапазоне
            for i in range((end - start).days + 1):
                d_ = start + timedelta(days=i)
                if d_ in booked:
                    await callback.answer(
                        "⛔ В выбранном диапазоне есть занятые даты",
                        show_alert=True
                    )
                    return
            await state.update_data(check_in=start, check_out=end)

        # Если обе даты уже были — сбрасываем и ставим новую check_in
        else:
            await state.update_data(check_in=selected, check_out=None)

    # Обновляем клавиатуру
    new = await state.get_data()
    kb = input_date_keyboard(
        year=selected.year,
        month=selected.month,
        check_in=new.get("check_in"),
        check_out=new.get("check_out"),
        booked_dates=booked
    )
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()




@router.callback_query(F.data.startswith("switch"))
async def switch_month(callback: types.CallbackQuery, state: FSMContext):
    _, year, month = callback.data.split("|")
    year, month = int(year), int(month)

    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    booked = set(data.get("booked_dates", []))

    markup = input_date_keyboard(
        year = year,
        month = month,
        check_in=check_in,
        check_out=check_out,
        booked_dates=booked,
    )

    await callback.message.edit_reply_markup(reply_markup=markup)


