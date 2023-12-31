from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

import text

router = Router()


@router.callback_query(Text("generate_map"))
async def map_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text.maps_generation)
    await callback.message.answer("https://www.google.com/maps/d/u/1/edit?mid=1HrloNMAd1cBWkZKt2_AmSl7S9uXwcqo&usp=sharing")
