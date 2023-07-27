import uuid
from datetime import datetime, timezone

from aiogram import F, Router, Bot
from aiogram.fsm import state
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from shapely import Point

from app_context import get_app_context
from repositories import ReportStatus, IncidentReport, User, UserStatus

router = Router()


class LeaveReportScene(state.StatesGroup):
    CONTACTS = state.State()
    LOCATION = state.State()
    PHOTOS = state.State()
    NEUTRALIZED = state.State()


@router.callback_query(Text("register_report"))
async def leave_report_handler(callback: CallbackQuery, state: FSMContext) -> None:
    tg_user_id = callback.from_user.id
    app_context = get_app_context()
    async with app_context.user_repository() as user_repo:
        user = await user_repo.get_by_telegram_id(tg_id=tg_user_id)
        if user is not None:
            async with app_context.report_repository() as report_repo:
                count = await report_repo.count_pending_reports_for_user(requested_by=user.id)
                if count == 3:
                    # To prevent spam
                    await callback.message.answer(
                        "Зачекайте поки переглянуть ваші попередні репорти."
                    )
                    return

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
    app_context = get_app_context()

    async with app_context.user_repository() as repo:
        user = await repo.get_by_telegram_id(tg_id=message.from_user.id)
        if user is None:
            user = User(
                id=uuid.uuid4(),
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                phone=message.contact.phone_number,
                status=UserStatus.DEFAULT
            )
        else:
            user.username = message.from_user.username
            user.phone = message.contact.phone_number

        await repo.save(user=user)

    await state.update_data(user=user)
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


@router.message(LeaveReportScene.PHOTOS, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    # TODO: Update handler to accept up to 5 photos.
    photos = (await state.get_data()).get('photos', [])
    best_res = message.photo[-1]
    photos.append(best_res)
    await state.update_data(photos=photos)

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
async def process_neutralized(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(neutralized=message.text.casefold() == 'так')
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Чудово, зберігаю ваш репорт",
        reply_markup=ReplyKeyboardRemove(),
    )

    app_context = get_app_context()
    "/opt/app/toxic-map/<report_uuid>/int"
    for photo in data["photos"]:
        # TODO: Actually download file to local filesystem.
        await bot.download(photo.file_id, '')

    location = Point(data["location"].longitude, data['location'].latitude)
    report = IncidentReport(
        id=uuid.uuid4(),
        reported_by=data["user"].id,
        location=location.wkt,
        photos=[],
        status=ReportStatus.PENDING,
        poison_removed=data["neutralized"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    async with app_context.report_repository as repo:
        await repo.save(report=report)

    await message.answer(text='Thanks for the report.')
