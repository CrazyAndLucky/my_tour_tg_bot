from aiogram.utils.keyboard import InlineKeyboardBuilder, CallbackData


class Product_cb(CallbackData, prefix='category'):
    id: str
    action: str


# Кнопи под товарами для пользователей
def product_markup_from_cart(idx, count, count_of: bool=False):
    builder = InlineKeyboardBuilder()
    
    if count_of == False:

        builder.button(text='⬅️', callback_data=Product_cb(id=idx, action='decrease'))
        builder.button(text=str(count), callback_data=Product_cb(id=idx, action='count'))
        builder.button(text='➡️', callback_data=Product_cb(id=idx, action='increase'))
    
    else:
        builder.button(text=str(count), callback_data=Product_cb(id=idx, action='count'))

    return builder.as_markup()