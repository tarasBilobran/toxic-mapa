from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import keyboards
import text

from . import _map, _contacts, _report_poison, _my_dog_is_poisoned, _describe_symptoms

ROOT_ROUTER = Router()
ROOT_ROUTER.include_routers(
    _map.router,
    _contacts.router,
    _report_poison.router,
    _my_dog_is_poisoned.router,
    _describe_symptoms.router,
)


@ROOT_ROUTER.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        text.greet.format(name=message.from_user.full_name), reply_markup=keyboards.menu
    )


@ROOT_ROUTER.message(F.text == "Меню")
@ROOT_ROUTER.message(F.text == "Вийти в меню")
@ROOT_ROUTER.message(F.text == "◀️ Вийти в меню")
async def menu(message: Message) -> None:
    await message.answer(text.menu, reply_markup=keyboards.menu)
