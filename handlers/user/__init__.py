from . import command, about_us, our_contacts, delete_message, my_booking

routers_from_user = [
    command.router,
    about_us.router,
    our_contacts.router,
    delete_message.router,
    my_booking.router,
]