from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "delete_message")
async def delete_message(callback:CallbackQuery):

    # to_msg
    await callback.message.delete()

