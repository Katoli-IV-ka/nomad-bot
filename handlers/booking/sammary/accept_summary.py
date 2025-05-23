from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from contents.booking.summary_contents import accept_summary_text, accept_summary_photo
from contents.menu.menu_contents import menu_keyboard
from database.notion_connect import update_verification_by_page_id
from handlers.verification.to_verify_booking import to_verify_booking

router = Router()

@router.callback_query(F.data == "accept_summary")
async def accept_summary(callback: CallbackQuery, state: FSMContext, bot: Bot=None):
    data = await state.get_data()
    notion_page_id = data.get('notion_page_id')

    update_verification_by_page_id(
        page_id=notion_page_id,
        new_status="On verification"
    )

    process_message = data.get("process_message")

    await process_message.edit_media(
        media=InputMediaPhoto(
            media=accept_summary_photo,
            caption=accept_summary_text,
            parse_mode="HTML",
        ),
        reply_markup=menu_keyboard()
    )

    await to_verify_booking(state=state, bot=bot)




