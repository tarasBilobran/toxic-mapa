from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    [InlineKeyboardButton(text="🔎 Мапа отруєнь Львів та околиці.", callback_data="generate_map"), ],
    [InlineKeyboardButton(text="✏️ Повідомити про локацію отрути.", callback_data="register_report")],
    [InlineKeyboardButton(text="🆘 Моя собака постраждала від отруєння.", callback_data="help_dog"), ],
    [InlineKeyboardButton(text="☣️ Симптоми отруєння", callback_data="describe_symptoms"), ],
    [InlineKeyboardButton(text="☎️ Контакти цілодобових вет-клінік.", callback_data="contacts")],
]
menu = InlineKeyboardMarkup(inline_keyboard=buttons)

poisoned_dog_buttons = [
    [InlineKeyboardButton(text="✏️ Повідомити про локацію отрути.", callback_data="register_report")],
    [InlineKeyboardButton(text="Продовжити.", callback_data="ask_dog_status")]
]
data = InlineKeyboardMarkup(inline_keyboard=poisoned_dog_buttons)


ask_dog_state_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Собака була отруєна, але вижила', callback_data='dog_survived')],
        [InlineKeyboardButton(text='Собака загинула від отруєння', callback_data='dog_died')],
    ]
)
