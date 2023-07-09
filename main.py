import logging
import os
from pathlib import Path

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackContext, \
    ConversationHandler, filters

from contacts import vet_clinics_contacts
from maps import poison_map
from report_conversation import REPORT_CONVERSATION, REPORT_HANDLER, REPORT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DIR = Path(__file__).parent / "tmp"

CHOOSING, REPORT_INCIDENT = range(2)

TOKEN = os.getenv("TG_TOKEN")
if TOKEN is None:
    raise NotImplementedError

KEYBOARD = [
    [KeyboardButton(text="Мапа отруєнь Львів та околиці.")],
    [KeyboardButton(text=REPORT)],
    # TODO: Implement case below once more details provided
    [KeyboardButton(text="Моя собака постраждала від отруєння.")],
    [KeyboardButton(text="Контакти цілодобових вет клінік.")]
]
MARKUP = ReplyKeyboardMarkup(KEYBOARD, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вибери потрібну опцію в меню.",
        reply_markup=MARKUP
    )

    return CHOOSING


# TODO: https://docs.python-telegram-bot.org/en/stable/examples.nestedconversationbot.html
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    map_handler = MessageHandler(filters.Regex("^Мапа отруєнь Львів та околиці.$"), poison_map)
    contacts_handler = MessageHandler(
        filters.Regex("^Контакти цілодобових вет клінік.$"),
        vet_clinics_contacts
    )

    application.add_handler(start_handler)
    application.add_handler(contacts_handler)
    application.add_handler(map_handler)
    application.add_handler(REPORT_HANDLER)
    application.add_handler(REPORT_CONVERSATION)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
