import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
)

from repository import IncidentReport

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

SENDING_PHOTOS, SENDING_LOCATION = 0, 1
SHARE_LOCATION = "Поділитися локацією."
SHARE_PHOTOS = "Надіслати фото."

REPORT = "Повідомити про локацію отрути."


async def report_incident(update: Update, context: CallbackContext):
    keyboard = [
        [
            KeyboardButton(text=SHARE_LOCATION, request_location=True),
            KeyboardButton(text=SHARE_PHOTOS),
        ],
        [KeyboardButton(text="Назад")],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ви можете поділитися фото та локацією.",
        reply_markup=reply_markup,
    )
    logging.info(update.message)
    return 0


async def share_photos(update: Update, context: CallbackContext):
    # TODO: Accept photos from TG bot
    # Receive up 5 photos
    print()
    response = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Завантажте фотографії",
    )


async def share_location(update: Update, context: CallbackContext):
    # TODO: Accept location from TG bot
    user_location = update.message.location
    incident_report = IncidentReport()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Геолокацію отримано",
    )


REPORT_HANDLER = MessageHandler(filters.Regex(f"^{REPORT}$"), report_incident)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("FINISH")
    await update.message.reply_text(
        f"Finish.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


REPORT_CONVERSATION = ConversationHandler(
    entry_points=[REPORT_HANDLER],
    states={
        0: [
            MessageHandler(filters.Regex(f"^{SHARE_LOCATION}$"), share_location),
            MessageHandler(filters.Regex(f"^{SHARE_PHOTOS}$"), share_photos),
        ]
    },
    fallbacks=[MessageHandler(filters.Regex("^Назад$"), done)],
    # persistent=True,
)
