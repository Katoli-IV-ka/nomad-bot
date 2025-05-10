import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

DEV_TELEGRAM_USER_ID = str(os.getenv("DEV_TELEGRAM_USER_ID"))
ADMINS_CHAT = int(os.getenv("ADMINS_CHAT"))
STAFF_TELEGRAM_ID = int(os.getenv("STAFF_TELEGRAM_ID"))

PRICES = {
    "weekday_price":           int(os.getenv("WEEKDAY_PRICE",       0)),
    "weekend_price":           int(os.getenv("WEEKEND_PRICE",      0)),
    "koupel_price":            int(os.getenv("KOUPLE_PRICE",       0)),
    "child_fee":               int(os.getenv("CHILD_FEE",          0)),
    "pet_fee":                 int(os.getenv("PET_FEE",            0)),
    "discount_threshold_days": int(os.getenv("DISCOUNT_THRESHOLD_DAYS", 0)),
    "discount_rate":           float(os.getenv("DISCOUNT_RATE",    0.0)),
}