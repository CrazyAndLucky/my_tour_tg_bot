from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from loader import db


class Category_cb(CallbackData, prefix='category'):
    id: str
    action: str


# Клавиатура для отображения категорий для пользователя
def categories_markup():
    builder = InlineKeyboardBuilder()

    for idx, title in db.fetchall('SELECT * FROM categories'):
        builder.button(text=title, callback_data=Category_cb(id=idx, action='view'))
        builder.adjust(1)

    return builder.as_markup()