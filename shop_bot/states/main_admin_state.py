from aiogram.fsm.state import State, StatesGroup

class Add_admin_state(StatesGroup):
    name = State()


class Del_admin_state(StatesGroup):
    name = State()


class Mailling_state(StatesGroup):
    message = State()
    confitm = State()