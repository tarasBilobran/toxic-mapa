from telegram import Update
from telegram.ext import CallbackContext


async def poison_map(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Генерую мапу.",
    )
    # TODO: Generate link to Google maps where all locations are marked using points.
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='http://www.google.com/maps/place/49.46800006494457,17.11514008755796'
    )
