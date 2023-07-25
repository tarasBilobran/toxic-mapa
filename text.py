greet = "Привіт, {name}, я бот, який допоможе зберегти життя собак ☺️"
menu = "📍 Головне меню"
report = "Відправте фото та локацію"
report_location = "Локацію збережено"
report_photo = "Фото збережено"
contacts = [
    "💊 Євровет вул. Пасічна, 102\n+380 (67) 559 69 08",
    "💊 Євровет вул.Яблонської, 8\n+ 380(67) 559 69 02",
    "💊 Вет клініка доктора Маркевича вул. Лисеницька, 2а\n+380 (68) 151 51 55",
    "💊 Ветмедкомплекс вул. Бучми, 22\n+380 (97) 233 98 17,",
    "💊 Алден-вет вул. Кульпарківська, 160\n +380 (68) 011 67 07",
]
an_incident = """
Нам дуже шкода, що це трапилось з вашим улюбленцем 😢 Будь ласка, слідуйте інструкціям

🏥 Якщо вет клініка недалеко, негайно їдьте туди! 

Якщо отрута була у вигляді таблеток (напр. у сосисках, хлібі, паштеті) це може бути протитуберкульозний препарат ізоніазид, або препарат метоклопрамід. 

‼️ Від ізоніазиду існує антидот, це пиридоксин (вітамін В6 в ампулах). Проте якщо собака має велику вагу, колоти його буде боляче, ампули продаються по 1 мл, і потрібно вколоти 1 мл на 1 кг маси собаки, чергуючи лапи. Тому швидше і ефективніше буде доїхати до вет клініки, якщо є можливість. Якщо можливості немає, слідуйте інструкціям нижче.

АНТИДОТ 💉:

якщо собака з'їла, облизала, обнюхала цю отруту, необхідно якнайшвидше вколоти пиридоксин (вітамін В6) 1мл на 1кг ваги собаки. Найкраще внутрішньовенно, але можна і мʼязево

оберіть наймʼякіше місце в мʼязі задньої лапки. Коліть в це місце на одній лапці, потім в іншій. Чергуйте. Не переживайте, що можете вколоти неправильно, ліпше вколоти непрофесійно, ніж не вколоти зовсім. Передозування цим препаратом зробити важко, тому не бійтеся, що вколете забагато

Метоклопрамід

розпізнати і відрізнити від ізоніазиду неможливо, це також таблетки! 

паралізує дихальну систему

АНТИДОТ 💉:

допомогу можуть надати ЛИШЕ у вет клініці

Щуряча отрута

Яскраво-рожеві сосиски, хліб, паштет, їжа з рожевим відтінком


АНТИДОТ 💉:

допомогу можуть надати ЛИШЕ у вет клініці

❗️У будь-якому випадку, якщо у собаки є симптоми отруєння (понос, судоми, надмірна млявість, часте сечовипускання), одразу їдьте до ветеринарної клініки! 

❗️Якщо вже пізній час, або комендантська година, везіть собаку в одну з цілодобових клінік. 

# TODO: link_to_clinics


❗️Залишайтесь на зв'язку з ветеринаром, дотримуйтесь усіх рекомендацій лікаря.

❗️Будь ласка, додайте адресу, за якою була розкинута отрута (хоча б приблизно) у наш бот. Для цього натисніть
# TODO: (тут додати кнопку щоб зарепортити)
"""
maps_generation = "Генерую мапу"

poison_symptoms = """
Ізоніазид (протитуберкульозний препарат):

Найчастіше: конвульсії, втрата координації, часте сечовипускання або дефекація, судоми.

Інші симптоми:

- Нудота та блювання
- Понос
- Загальна слабкість та втрата координації
- Запаморочення та судоми
- Підвищена температура тіла
- Подавлення дихання
- Збудження та неспокій
- Зміна апетиту (від відсутності апетиту до підвищеного апетиту)
- Поліурія (збільшення кількості виділеної сечі)
- Розмитий зір або втрата зору

АНТИДОТ 💉:

якщо собака з'їла, облизала, обнюхала цю отруту, необхідно якнайшвидше вколоти пиридоксин (вітамін В6) 1мл на 1кг ваги собаки. Найкраще внутрішньовенно, але можна і мʼязево

оберіть наймʼякіше місце в мʼязі задньої лапки. Коліть в це місце на одній лапці, потім в іншій. Чергуйте. Не переживайте, що можете вколоти неправильно, ліпше вколоти непрофесійно, ніж не вколоти зовсім. Передозування цим препаратом зробити важко, тому не бійтеся, що вколете забагато

Щуряча отрута:

Щуряча отрута містить антикоагулянти, які не дають звертатися крові. Тут ми будемо мати внутрішню кровотечу з великою вірогідністю.

 - Кровотечі: можуть бути видимі кровотечі з носа, ясен, шкіри або внутрішні кровотечі, що виявляються у вигляді кров'яних викидень, темного калу або крові у сечі.
 - Загальна слабкість та втрата координації: собака може стати слабкою, втратити інтерес до активностей, мати проблеми з рухом та координацією.
 - Зниження апетиту та втрата ваги: собака може відмовлятися від їжі та поступово втрачати вагу.
 - Блювання та діарея: можуть спостерігатися часті блювання та понос.
 - Загальна депресія: собака може проявляти сонливість, втрату інтересу до оточуючого середовища та пасивність.
 - Нестабільна ходьба та тремори: можуть виникнути проблеми з рухом, незримі судоми та тремори.

АНТИДОТ💉: 

Протиотрута існує, але колоти має ЛИШЕ лікар вет медицини, тому якнайшвидше їдьте в лікарню і опишіть симптоми, ветеринар знатиме, як допомогти

 Метоклопрамід

В результаті отруєння паралізується дихальна система, від чого тварина помирає у найближчі дні

АНТИДОТ 💉:

допомогу можуть надати ЛИШЕ у вет клініці
"""
greet_admin = "Привіт, {name}. Є {count} репортів котрі потрібно переглянути?"
admin_report_accept = "Підтвердити"
admin_report_reject = "Відхилити"
admin_report_reject_and_block = "Відхилити та заблокувати користувача"
