from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    REGISTER = State()
    EXPENSE = State()
    SET_EXPENSE = State()
    GET_EXPENSE = State()
    GET_EXPENSE_PERIOD = State()
    SET_EXPENSE_CHECK = State()
