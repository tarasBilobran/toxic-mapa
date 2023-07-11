from aiogram.fsm import state


class LeaveReportScene(state.StatesGroup):
    CONTACTS = state.State()
    LOCATION = state.State()
    PHOTOS = state.State()
    NEUTRALIZED = state.State()
