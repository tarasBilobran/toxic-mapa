from datetime import datetime, timezone

import shapely
from aiogram import F, Router
from aiogram.fsm import state
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, FSInputFile

import text
from app_context import get_app_context
from keyboards import admin_menu_keyboard
from repositories import UserStatus, ReportStatus, IncidentReport

router = Router()


class AdminReportState(state.StatesGroup):
    DECISION = state.State()


@router.callback_query(Text("admin_reports_list"))
async def reports_list_handler(callback: CallbackQuery, state: FSMContext) -> None:
    app_context = get_app_context()

    async with app_context.report_repository() as repo:
        report = await repo.get_pending_report()

    if report is None:
        await callback.message.answer("Доступних репортів немає.")
        return

    report: IncidentReport
    await callback.message.answer(f"Report from user {report.reported_by}")

    point = shapely.from_wkt(report.location)
    await callback.message.answer_location(latitude=point.x, longitude=point.y)

    media_group = []
    for file in report.photos:
        media_group.append(InputMediaPhoto(
            media=FSInputFile(file)
        ))

    await callback.message.answer("Фото котрі користувач додав:")
    await callback.message.answer_media_group(media_group)

    if report.poison_removed:
        await callback.message.answer("Отруту було прибрано.")
    else:
        await callback.message.answer("Отруту не було прибрано.")

    await state.set_state(AdminReportState.DECISION)
    await state.set_data(report=report)
    await callback.message.answer("Що робити із репортом?",
                                  reply_markup=ReplyKeyboardMarkup(
                                      keyboard=[
                                          [
                                              KeyboardButton(text=text.admin_report_accept),
                                              KeyboardButton(text=text.admin_report_reject),
                                              KeyboardButton(text=text.admin_report_reject_and_block)
                                          ]
                                      ],
                                      resize_keyboard=True, one_time_keyboard=True
                                  ),
                                  )


@router.message(AdminReportState.DECISION, F.text == text.admin_report_accept)
# TODO Тут в мене є файний приклад як дока мені напиздюнькала і я проїбав +-2 години часу)
async def process_report_accept(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    report: IncidentReport = data["report"]
    report.status = ReportStatus.ACTIVE
    report.updated_at = datetime.now(timezone.utc)

    app_context = get_app_context()
    async with app_context.report_repository() as repo:
        await repo.save(report)

    await message.answer(
        "Підтверджено та збережено", reply_markup=admin_menu_keyboard
    )


@router.message(AdminReportState.DECISION, F.text == text.admin_report_reject)
async def process_report_reject(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    report: IncidentReport = data["report"]

    app_context = get_app_context()
    async with app_context.report_repository() as repo:
        await repo.delete_by_id(report.id)

    await message.answer(
        "Відхилено та видалено", reply_markup=admin_menu_keyboard
    )


@router.message(AdminReportState.DECISION, F.text == text.admin_report_reject_and_block)
async def process_report_reject_and_block(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    report: IncidentReport = data["report"]

    app_context = get_app_context()
    async with app_context.report_repository() as repo:
        await repo.delete_by_reported_by(reported_by=report.reported_by)

    async with app_context.user_repository() as repo:
        user = await repo.get(id=report.reported_by)
        user.status = UserStatus.BLOCKED
        await repo.save(user=user)

    await message.answer(
        "Відхилено, видалено та заблоковано користувача", reply_markup=admin_menu_keyboard
    )
