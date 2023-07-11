from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="🔎 Мапа отруєнь Львів та околиці.", callback_data="generate_map"),],
    [InlineKeyboardButton(text="✏️ Повідомити про локацію отрути.", callback_data="register_report")],
    [InlineKeyboardButton(text="🆘 Моя собака постраждала від отруєння.", callback_data="help_dog"),],
    [InlineKeyboardButton(text="☣️ Симптоми отруєння", callback_data="describe_symptoms"),],
    [InlineKeyboardButton(text="☎️ Контакти цілодобових вет-клінік.", callback_data="contacts")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
# exit_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Вийти в меню")]], resize_keyboard=True)
# iexit_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️  Вийти в меню",
#                                                                              callback_data="menu")]])

report = [
    # [InlineKeyboardButton(text="Відправити локацію", request_location=True), InlineKeyboardButton(text="Відправити фото")],
    [InlineKeyboardButton(text="◀️ Вийти в меню", callback_data="generate_map")]
]
replay_report = InlineKeyboardMarkup(inline_keyboard=report)
