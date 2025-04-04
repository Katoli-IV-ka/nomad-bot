from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database.notion_connect import add_row
from keyboards.menu_kb import reply_menu_keyboard, menu_keyboard
from keyboards.summary_kb import summary_keyboard
from messages.summary_msg import get_summary_message
from states.booking_states import BookingState
from utils.calculate_booking_price import calculate_booking_price

router = Router()

@router.message(BookingState.share_contact, F.contact)
async def receive_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    username = message.from_user.username

    await state.update_data(
        phone_number=contact.phone_number,
        first_name=contact.first_name,
        tg_user_id=contact.user_id,
        username=username
    )

    data = await state.get_data()
    choice_options_msg = data.get("choice_options_msg", None)
    if choice_options_msg:
        await choice_options_msg.delete()
    if message.reply_to_message:
        await message.reply_to_message.delete()


    # to_msg
    await message.answer(
        text = f"Спасибо! Контакт сохранён.\n{contact.first_name}\n{contact.phone_number}",
        #reply_markup = reply_menu_keyboard()
    )


    await state.set_state(BookingState.summary)

    # Получаем всё из состояния
    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    package = data.get("package_options", {})
    contact_data = {
        "first_name": contact.first_name + (" " + message.from_user.last_name if message.from_user.last_name else ""),
        "phone_number": contact.phone_number,
        "user_id": message.from_user.id,
    }



    total = calculate_booking_price(check_in, check_out, package)
    summary = get_summary_message(check_in, check_out, package, contact_data, username, total)


    response = add_row({
        "id": str(contact_data["user_id"]),
        "phone": str(contact_data["phone_number"]),
        "start_date": str(check_in),
        "end_date": str(check_out),
        "cost": total,
        "contact": str(contact_data["first_name"]),
        'kids': package['child'],
        'pet': package['pet'],
        'koupel': package['koupel'],
        'num_quests': '1' if package['one_person'] is True else '2',
    })


    await state.update_data(data_id = response["id"])

    await message.answer_photo(
        photo = "AgACAgIAAxkBAAIByWfrCv-oNYvy842u29I6r1GG6etVAAKu9TEb4TZZS7UhzXPay0zqAQADAgADcwADNgQ",
        caption = summary,
        reply_markup=summary_keyboard(),
        parse_mode="Markdown"
    )



    await message.delete()



@router.message(BookingState.shooting_share_contact, F.contact)
async def receive_shooting_contact(message: types.Message, state: FSMContext):
    contact = message.contact

    await state.update_data(
        phone_number=contact.phone_number,
        first_name=contact.first_name,
        tg_user_id=contact.user_id
    )


    # Получаем всё из состояния
    data = await state.get_data()
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    contact_data = {
        "first_name": contact.first_name + (" " + message.from_user.last_name if message.from_user.last_name else ""),
        "phone_number": contact.phone_number,
        "user_id": message.from_user.id,
    }

    response = add_row({
        "id": str(contact_data["user_id"]),
        "phone": str(contact_data["phone_number"]),
        "start_date": str(check_in),
        "end_date": str(check_out),
        "contact": str(contact_data["first_name"]),
        'shooting': True,
    })



    # to_msg
    await message.answer_photo(
        photo="AgACAgIAAxkBAAIBy2frCwgummI8aLSuDkAhkFsxp94hAAKv9TEb4TZZS2ezt3UE4RvuAQADAgADcwADNgQ",
        caption="📲 Спасибо! Ваша заявка отправлена. Менеджер свяжется с вами в ближайшее время.",
        reply_markup=menu_keyboard()
    )