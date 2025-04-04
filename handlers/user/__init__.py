from . import command, about_us, our_contacts, delete_message

routers_from_user = [
    command.router,
    about_us.router,
    our_contacts.router,
    delete_message.router,
]