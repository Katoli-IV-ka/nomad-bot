from . import wait_payment, reject_booking, to_verify_booking, confirm_payment

routers_from_verification = [
    confirm_payment.router,
    wait_payment.router,
    reject_booking.router,
    to_verify_booking.router,
]