from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back_message = '👈 Назад'
all_right_message = '✅ Все верно'
confirm_message = '✅ Подтвердить заказ'

accounts = '📋 Товары'
reviews = '💬 Канал с отзывами'
reference = '🗂 Справка'
help_button = '🙌 Помощь'

add_account = '➕ Добавить товар'
orders = '🛒 Активные заказы'

admins = '☢️ Админы'
mailling = '✉️ Рассылка по пользователям'



# Клавиатура для возврата на предыдущий шаг при создании товара
def back_markup():
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=back_message)]], 
                                                        resize_keyboard=True,
                                                        selective=True)
    return markup


def check_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_message), KeyboardButton(text=all_right_message)]],
        resize_keyboard=True     
        )
    
    return markup


def confirm_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_message), KeyboardButton(text=confirm_message)]], 
        resize_keyboard=True
        )
    return markup


# Клавиатура для меню пользователя
def menu_user_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=accounts), 
            KeyboardButton(text=reviews)], 
            [KeyboardButton(text=reference),
            KeyboardButton(text=help_button)],
            [KeyboardButton(text=orders)]
            ], 
        resize_keyboard=True
        )
    return markup


# Клавиатура для меню админа
def menu_admin_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=accounts), 
            KeyboardButton(text=orders)],
            ],  
        resize_keyboard=True
        )
    return markup

# Клавиатура для главного админа
def menu_main_admin_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=accounts), 
            KeyboardButton(text=orders)],
            [KeyboardButton(text=admins), 
            KeyboardButton(text=mailling)]
            ],  
        resize_keyboard=True
        )
    return markup    