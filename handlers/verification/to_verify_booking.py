from aiogram import F, types, Router, Bot
from aiogram.fsm.context import FSMContext

from config import ADMINS_CHAT
from contents.verification.booking_verification_contents import booking_confirmation_text, booking_confirmation_keyboard, \
    booking_confirmation_photo
from utils.calculate_booking_price import calculate_booking_price

router = Router()


@router.callback_query(F.data == "to_booking_confirmation")
async def to_verify_booking(state: FSMContext, callback: types.CallbackQuery = None, bot: Bot = None):
    data = await state.get_data()

    check_in = data.get("check_in")
    check_out = data.get("check_out")
    package = data.get("package_options", {})
    contact_name = data.get("contact_name")
    phone_number = data.get("phone_number")
    username = data.get("username")
    notion_page_id = data.get("notion_page_id")

    total = calculate_booking_price(check_in, check_out, package)

    await bot.send_photo(
        chat_id=ADMINS_CHAT,
        photo=booking_confirmation_photo,
        caption=booking_confirmation_text(
            check_in=check_in,
            check_out=check_out,
            package=package,
            contact_name=contact_name,
            phone_number=phone_number,
            username=username,
            total=total,
        ),
        reply_markup=booking_confirmation_keyboard(notion_page_id),
        parse_mode="Markdown"
    )
