import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DEV_TELEGRAM_USER_ID = str(os.getenv("DEV_TELEGRAM_USER_ID"))