from aiogram.fsm.state import State, StatesGroup

class Checkout_state(StatesGroup):
    check_cart = State()
    name = State()
    address = State()
    confirm = State()
 