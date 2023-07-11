from aiogram import F, Router, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

import keyboards
import text

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=keyboards.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Вийти в меню")
@router.message(F.text == "◀️ Вийти в меню")
async def menu(message: Message):
    await message.answer(text.menu, reply_markup=keyboards.menu)


@router.callback_query(Text("generate_map"))
async def map_handler(callback: CallbackQuery):
    await callback.message.answer(text.maps_generation)
    await callback.message.answer("Згенерована мапа")


@router.callback_query(Text("register_report"))
async def report_handler(callback: CallbackQuery):
    await callback.message.answer(text.report, reply_markup=keyboards.replay_report)


@router.callback_query(Text("help_dog"))
async def an_incident_handler(callback: CallbackQuery):
    await callback.message.answer(text.an_incident)


@router.callback_query(Text("describe_symptoms"))
async def describe_poison_symptoms(callback: CallbackQuery):
    await callback.message.answer(text.poison_symptoms)


@router.callback_query(Text("contacts"))
async def contacts_handler(callback: CallbackQuery):
    await callback.message.answer("🏥 Список цілодобових клінік у Львові:\n" + "\n".join(text.contacts))


@router.message(F.photo)
async def report_photo_handler(message: Message, bot: Bot):
    # TODO Save photo correctly
    await bot.download(
        message.photo[-1],
        destination=f"/tmp/{message.photo[-1].file_id}.jpg"
    )
    await message.answer(text.report_photo)


@router.message(F.location)
async def report_location_handler(message: Message):
    # TODO Save location correctly
    location = message.location
    await message.answer(text.report_location)
