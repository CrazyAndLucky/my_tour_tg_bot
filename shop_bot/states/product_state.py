from aiogram.fsm.state import State, StatesGroup

class CategoryState(StatesGroup):
    title = State()

class ProductState(StatesGroup):
    title = State()
    price = State()
    body = State()
    image = State()
    pay_link = State()

class Process_cart_state(StatesGroup):
    products = State()