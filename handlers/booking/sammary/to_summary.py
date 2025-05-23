from datetime import timedelta

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from contents.booking.summary_contents import get_summary_text, get_summary_keyboard, summary_photo
from database.notion_connect import add_row
from states.booking_states import BookingState
from utils.calculate_booking_price import calculate_booking_price


router = Router()

@router.callback_query(F.data == "to_summary")
async def to_summary(state: FSMContext, callback: types.CallbackQuery = None):
    await state.set_state(BookingState.summary)
    data = await state.get_data()

    if callback is not None:
        process_message = callback.message
    else:
        process_message = data.get("process_message")

    # Получаем все данные о бронировании из состояния
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    package = data.get("package_options", {})
    contact_name = data.get("contact_name")
    phone_number = data.get("phone_number")
    telegram_user_id = data.get("telegram_user_id")
    username = data.get("username")

    total = calculate_booking_price(check_in, check_out, package)

    await process_message.edit_media(
        media=InputMediaPhoto(
            media=summary_photo,
            caption=get_summary_text(
                check_in=check_in,
                check_out=check_out+timedelta(days=1),
                package=package,
                contact_name=contact_name,
                phone_number=phone_number,
                username=username,
                total=total
            ),
            parse_mode="HTML",
        ),
        reply_markup=get_summary_keyboard()
    )

    response = add_row({
        "id": str(telegram_user_id),
        "phone": str(phone_number),
        "start_date": str(check_in),
        "end_date": str(check_out),
        "cost": total,
        "contact": str(contact_name),
        'kids': package['child'],
        'pet': package['pet'],
        'koupel': package['koupel'],
        'num_quests': '1' if package['one_person'] is True else '2',
        'verify': 'Incomplete application',
    })

    await state.update_data(notion_page_id=response["id"])




