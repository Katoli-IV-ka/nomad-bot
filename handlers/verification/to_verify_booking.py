from datetime import timedelta

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

    user_id = callback.from_user.id
    photos = await bot.get_user_profile_photos(user_id, limit=1)

    if photos.total_count and photos.photos:
        # Берём самое большое фото из первой группы
        photo_size = photos.photos[0][-1]
        photo_id = photo_size.file_id
    else:
        photo_id = booking_confirmation_photo

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
        photo=photo_id,
        caption=booking_confirmation_text(
            check_in=check_in,
            check_out=check_out+timedelta(days=1),
            package=package,
            contact_name=contact_name,
            phone_number=phone_number,
            username=username,
            total=total,
        ),
        reply_markup=booking_confirmation_keyboard(notion_page_id),
        parse_mode="HTML"
    )
