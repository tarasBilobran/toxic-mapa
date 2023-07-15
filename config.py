import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_API_KEY")

# TODO Add your id for admin panel. Use https://t.me/getmyid_bot.
ADMINS = [781766999, ]
