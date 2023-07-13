from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import text

router = Router()


@router.callback_query(Text("ask_if_dog_is_fine"))
async def ask_about_dog_state(callback: CallbackQuery):
    await callback.message.answer(
        "Який стан вашої собаки?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Собака була отруєна, але вижила"),
                    KeyboardButton(text="Собака загинула від отруєння"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.callback_query(Text("help_dog"))
async def an_incident_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text.an_incident)

    label = "Ви можете повідомити про локацію отрути зараз або продовжути заповнювати форму."
    # TODO: fix this copy-paste
    button = InlineKeyboardButton(text="✏️ Повідомити про локацію отрути.", callback_data="register_report")
    await callback.message.answer(
        label,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [button],
            [InlineKeyboardButton(text="Продовжити.", callback="ask_if_dog_is_fine")]
        ])
    )


