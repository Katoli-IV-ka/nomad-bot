from . import input_date, choice_options_package, share_contact, back_to_options, cancel, pay_cash, pay_by_card

routers_from_booking = [
    input_date.router,
    choice_options_package.router,
    share_contact.router,
    back_to_options.router,
    cancel.router,
    pay_cash.router,
    pay_by_card.router,
]