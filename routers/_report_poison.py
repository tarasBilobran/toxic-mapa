from typing import Dict, Any

from aiogram import F, Router
from aiogram.fsm import state
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


router = Router()


class LeaveReportScene(state.StatesGroup):
    CONTACTS = state.State()
    LOCATION = state.State()
    PHOTOS = state.State()
    NEUTRALIZED = state.State()


@router.callback_query(Text("register_report"))
async def leave_report_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LeaveReportScene.CONTACTS)
    await callback.message.answer("Натисніть поділитись", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Поділитись контактом", request_contact=True),
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    ))


@router.message(LeaveReportScene.CONTACTS)
async def process_contacts(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Ми отримали контактні дані",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.update_data(name=message.from_user.full_name, username=message.from_user.username, phone=message.contact.phone_number)
    await state.set_state(LeaveReportScene.LOCATION)
    await message.answer("Поділіться локацією отрути", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Поділитись локацією", request_location=True),
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    ))


@router.message(LeaveReportScene.LOCATION, F.location)
async def process_location(message: Message, state: FSMContext) -> None:
    await state.update_data(location=message.location)
    await state.set_state(LeaveReportScene.PHOTOS)
    await message.answer("Отримали локацію, поділіться фото де саме розташована отрута")


# TODO Accept upload 5 photos
@router.message(LeaveReportScene.PHOTOS, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    await state.update_data(photo=message.photo)
    await state.set_state(LeaveReportScene.NEUTRALIZED)
    await message.answer(
        "Чи прибрали ви отруту?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Так"),
                    KeyboardButton(text="Ні"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(LeaveReportScene.NEUTRALIZED, F.text.casefold())
async def process_neutralized(message: Message, state: FSMContext) -> None:
    await state.update_data(neutralized=message.text.casefold())
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Чудово, зберігаю ваш репорт",
        reply_markup=ReplyKeyboardRemove(),
    )
    await save_report(message=message, data=data)


async def save_report(message: Message, data: Dict[str, Any]) -> None:
    print(data)
    name = data["name"]
    username = data["username"]
    phone = data["phone"]
    photo = data["photo"]
    location = data["location"]
    neutralized = data["neutralized"]
    text = f"Імя - {name}\n" \
           f"Юзернейм - {username}\n" \
           f"Телефон - {phone}\n" \
           f"Фото - {photo}\n" \
           f"Локація - {location}\n" \
           f"Знешкоджено - {neutralized}\n"
    await message.answer(text=text)

