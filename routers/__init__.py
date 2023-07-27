from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import keyboards
import text
from app_context import get_app_context
from repositories import UserStatus

from . import (_contacts, _describe_symptoms, _map, _my_dog_is_poisoned,
               _report_poison)
from .admin import _reports_list

ROOT_ROUTER = Router()
ROOT_ROUTER.include_routers(
    _map.router,
    _contacts.router,
    _report_poison.router,
    _my_dog_is_poisoned.router,
    _describe_symptoms.router,
    _reports_list.router
)


@ROOT_ROUTER.message(Command("start"))
async def start_handler(message: Message) -> None:
    context = get_app_context()
    async with context.user_repository() as repo:
        user = await repo.get_by_telegram_id(tg_id=message.from_user.id)

    if user is not None and user.status == UserStatus.BLOCKED:
        await message.answer("Ви заблоковані.")

    if user is not None and user.status == UserStatus.ADMIN:
        async with context.report_repository() as repo:
            reports_count = await repo.get_pending_reports_count()

        if reports_count:
            await message.answer(
                text.greet_admin.format(
                    name=message.from_user.full_name, count=reports_count),
                    reply_markup=keyboards.admin_menu_keyboard
            )
        else:
            await message.answer(
                "Вітаю, наразі немає жодного репорта до перевірки."
            )
    await message.answer(
        text.greet.format(name=message.from_user.full_name), reply_markup=keyboards.menu_keyboard
    )


@ROOT_ROUTER.message(F.text == "Меню")
@ROOT_ROUTER.message(F.text == "Вийти в меню")
@ROOT_ROUTER.message(F.text == "◀️ Вийти в меню")
async def menu(message: Message) -> None:
    await message.answer(text.menu, reply_markup=keyboards.menu_keyboard)
