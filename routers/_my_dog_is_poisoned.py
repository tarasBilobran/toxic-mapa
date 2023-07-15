from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

import text
import keyboards

router = Router()
dog_died_messages = [
"""
Якщо тварина загинула в ветеринарній клініці, то чекаємо заключення вет лікаря, де буде написано "Підозра на отруєння (вказати назву препарату або отрути)". 

❗️Обовʼязково вимагайте цього заключення із зазначенням підозри на певну речовину або препарат

❗️ Зберігайте усі описи стану і лікування, усі результати обстежень і аналізів

❗️Збережіть усі чеки з вет клініки і аптеки

❗️Необхідно зробити фото або відео тіла. Ми знаємо, що це дуже важко морально, проте просимо вас зафіксувати це, щоб подати заяву в поліцію

‼️ З усіма цими документами + документами власника, напишіть заяву в поліцію
""",
"""
Якщо тварина загинула не дійшовши до вет клініки:

❗️Викликати поліцію на місце і повідомити про потенційну локацію вигулу

Зробити фото мертвої тварини, а краще почати запис під час симптомів. Розуміємо, що це дуже важко, і щиро співчуваємо. Це необхідно для написання заяви.

❗️Якщо є можливість, тримайте тіло у холоді (можливо запропонують розтин і токсикологію)

❗️ З документами власника тварини, напишіть заяву в поліцію
"""
]

dog_survived_text = """
Якщо собаку було отруєно, і тварину врятували.

❗️Обов'язково вимагайте заключення вет лікаря, де буде написано "Підозра на отруєння (вказати назву препарату або отрути)". Це є підставою для написання заяви в поліцію

❗️Зберігайте усі описи стану і лікування, усі результати обстежень і аналізів

❗️Збережіть усі чеки з вет клініки і аптеки

❗️Необхідно зробити фото або відео, де буде видно симптоми

‼️З усіма цими документами + документами власника, напишіть заяву в поліцію
"""

docs_for_police_report = """
✍️ Які документи потрібні для написання заяви у поліцію:

1. Копія паспорта тварини
2. Копія  паспорта власника тварини
3. Копія витягу про місце реєстрації
4. Копія ідентифікаційного коду
"""


@router.callback_query(Text("dog_died"))
async def dog_died(callback: CallbackQuery):
    await callback.message.answer(dog_died_messages[0])
    await callback.message.answer(dog_died_messages[1])

    await callback.message.answer(docs_for_police_report)


@router.callback_query(Text("dog_survived"))
async def dog_survived(callback: CallbackQuery):
    await callback.message.answer(dog_survived_text)

    await callback.message.answer(docs_for_police_report)


@router.callback_query(Text("help_dog"))
async def an_incident_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text.an_incident)

    await callback.message.answer(
        'Придумати message тут.',
        reply_markup=keyboards.data,
    )


@router.callback_query(Text("ask_dog_status"))
async def ask_about_dog_state(callback: CallbackQuery):
    await callback.message.answer(
        "Який стан вашої собаки?",
        reply_markup=keyboards.ask_dog_state_kb,
    )

