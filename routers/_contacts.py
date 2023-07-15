from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

import text

router = Router()


@router.callback_query(Text("contacts"))
async def contacts_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "🏥 Список цілодобових клінік у Львові:\n" + "\n".join(text.contacts)
    )
    # TODO: Return to main menu?
