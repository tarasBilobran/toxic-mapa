from telegram import Update
from telegram.ext import CallbackContext


async def vet_clinics_contacts(update: Update, context: CallbackContext):
    text = "Контакти вет клінік:\n\n"
    clinics = [
        "Євровет вул. Пасічна, 102 +380 (67) 559 69 08",
        "Євровет вул.Яблонської, 8 + 380(67) 559 69 02",
        "Вет клініка доктора Маркевича вул. Лисеницька, 2а +380 (68) 151 51 55",
        "Ветмедкомплекс вул. Бучми, 22 +380 (97) 233 98 17",
        "Алден-вет вул. Кульпарківська, 160 +380 (68) 011 67 07"
    ]
    text += "\n".join(clinics)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )
