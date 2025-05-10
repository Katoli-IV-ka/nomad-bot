from datetime import date, timedelta
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from contents.booking.input_date_contents import input_date_keyboard
from utils.get_booked_dates import get_booking_dates

router = Router()


@router.callback_query(F.data.startswith("select"))
async def select_date(callback, state: FSMContext):
    # Вытаскиваем из state
    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    booked = set(data.get("booked_dates", []))

    # распарсим callback
    _, y, m, d = callback.data.split("|")
    selected = date(int(y), int(m), int(d))

    # если день занят — блокируем
    if selected in booked:
        await callback.answer("⛔ Дата недоступна", show_alert=True)
        return

    # если ещё нет ни одной даты — ставим check_in
    if check_in is None and check_out is None:
        await state.update_data(check_in=selected)

    # если уже есть только check_in — ставим вторую и нормализуем порядок
    elif check_in is not None and check_out is None:
        # определяем границы
        start, end = sorted([check_in, selected])
        # проверяем любой конфликт
        for i in range((end - start).days + 1):
            d_ = start + timedelta(days=i)
            if d_ in booked:
                await callback.answer("⛔ В выбранном диапазоне есть занятые даты", show_alert=True)
                return
        # сохраняем оба
        await state.update_data(check_in=start, check_out=end)

    # если уже были обе даты — сбрасываем и ставим новую check_in
    else:
        await state.update_data(check_in=selected, check_out=None)

    # обновляем клавиатуру
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

    markup = input_date_keyboard(
        year = year,
        month = month,
        check_in=data.get("check_in"),
        check_out=data.get("check_out"),
        booked_dates=await get_booking_dates(),
    )

    await callback.message.edit_reply_markup(reply_markup=markup)


