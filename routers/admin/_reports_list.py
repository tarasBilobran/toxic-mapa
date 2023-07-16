from aiogram import F, Router
from aiogram.fsm import state
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import text
from keyboards import admin_menu_keyboard

router = Router()


class AdminReportState(state.StatesGroup):
    DECISION = state.State()


@router.callback_query(Text("admin_reports_list"))
async def reports_list_handler(callback: CallbackQuery, state: FSMContext) -> None:
    # TODO Here we need to request only one unreviewed report in this logic
    await state.set_state(AdminReportState.DECISION)
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


@router.message(AdminReportState.DECISION)
# TODO Тут в мене є файний приклад як дока мені напиздюнькала і я проїбав +-2 години часу)
@router.message(F.text.casefold() == text.admin_report_accept)
async def process_report_accept(message: Message, state: FSMContext) -> None:
    # TODO Add to report status approved
    await message.answer(
        "Підтверджено та збережено", reply_markup=admin_menu_keyboard
    )


@router.message(AdminReportState.DECISION)
@router.message(F.text.casefold() == text.admin_report_reject)
async def process_report_reject(message: Message, state: FSMContext) -> None:
    # TODO Add deleting report from database, or mark as reject
    await message.answer(
        "Відхилено та видалено", reply_markup=admin_menu_keyboard
    )


@router.message(AdminReportState.DECISION)
@router.message(F.text.casefold() == text.admin_report_reject_and_block)
async def process_report_reject_and_block(message: Message, state: FSMContext) -> None:
    # TODO Add deleting report from database or mark as reject, and block user.
    await message.answer(
        "Відхилено, видалено та заблоковано користувача", reply_markup=admin_menu_keyboard
    )
