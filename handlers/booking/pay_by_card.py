from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from utils.calculate_booking_price import calculate_booking_price

router = Router()

@router.callback_query(F.data == "pay_by_card")
async def handle_card_payment(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total = calculate_booking_price(data["check_in"], data["check_out"], data["package_options"])

    # Уникальный идентификатор заказа (можно заменить на ID из БД)
    user_id = callback.from_user.id
    order_id = f"{user_id}-{int(data['check_in'].strftime('%Y%m%d'))}"

    # Пример ссылки (здесь можно подключить реальный Alfa API)
    payment_link = f"https://pay.example.com/alfa?order_id={order_id}&amount={total}"

    await callback.message.edit_text(
        f"💳 Для оплаты нажмите на кнопку ниже:\n\n"
        f"[Перейти к оплате]({payment_link})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )