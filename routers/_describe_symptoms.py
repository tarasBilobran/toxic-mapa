from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

import text

router = Router()


@router.callback_query(Text("describe_symptoms"))
async def describe_poison_symptoms(callback: CallbackQuery) -> None:
    await callback.message.answer(text.poison_symptoms)

