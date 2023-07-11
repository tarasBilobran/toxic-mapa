import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_API_KEY")
