from aiogram.utils.keyboard import InlineKeyboardBuilder

from .categories import Category_cb
from loader import db


# Кнопки для добавления в корзину
def product_markup_from_catalog(idx='', price=0):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f'Добавить в корзину - {price}₽',
        callback_data=Category_cb(id=idx, action='add')
        )
    
    return builder.as_markup()