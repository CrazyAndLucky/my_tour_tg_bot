from aiogram.types import Message, BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import F

from loader import dp, db
from shop_bot.filters import IsAdmin
from shop_bot.keyboards.default.markups import orders


class Product_cb(CallbackData, prefix='product'):
    idx: str
    action: str


# Отображение активных заказов для админа
@dp.message(IsAdmin(), F.text == orders)
async def orders_button(message: Message):
    usr_orders = await db.fetchall('SELECT * FROM orders')
    if len(usr_orders) == 0:
        await message.answer('Пока нет активных заказов')
    else:

        for usr_order in usr_orders:
            usr_id = usr_order[0]
            idx = usr_order[1]
            title = usr_order[2]
            body = usr_order[3]
            photo = usr_order[4]
            price = usr_order[5]

            
            text = f'Заказ сделал: <a href="tg://user?id={usr_id}"><b>ССЫЛКА НА ПРОФИЛЬ</b></a>\n\n{title}\n\n{price}\n\n{body}'

            await message.answer_photo(
                photo=BufferedInputFile(file=photo, filename='image'),
                caption=text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Заказ выполнил', callback_data=Product_cb(idx=idx, action='order').pack())],
                    [InlineKeyboardButton(text='Вернуть заказ в продажу', callback_data=Product_cb(idx=idx, action='back_order').pack())],
                    ])
                )
            

# Подтверждение выпонения заказа
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'order'))
async def order_confirm(query: CallbackQuery, callback_data: Product_cb):
    idx = callback_data.idx
    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Подтвердить выполнение заказа', callback_data=Product_cb(idx=idx, action='confirm_order').pack())], [InlineKeyboardButton(text='👈 Назад', callback_data=Product_cb(idx=idx, action='back').pack())]]))


# Отмена подтверждения
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'back'))
async def back_order_confirm(query: CallbackQuery, callback_data: Product_cb):
    idx = callback_data.idx
    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заказ выполнил', callback_data=Product_cb(idx=idx, action='order').pack())],
        [InlineKeyboardButton(text='Вернуть заказ в продажу', callback_data=Product_cb(idx=idx, action='back_order').pack())]
        ]))


# Подтверждение выполнения заказа
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'confirm_order'))
async def order_confirm(query: CallbackQuery, callback_data: Product_cb):
    idx = callback_data.idx
    await query.message.delete()

    await db.query('DELETE FROM orders WHERE idx = ?', (idx,))

    await query.message.answer(text='✅ ЗАКАЗ ВЫПОЛНЕН ✅')


# Возвращение заказа в продажу
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'back_order'))
async def order_confirm(query: CallbackQuery, callback_data: Product_cb):
    idx = callback_data.idx
    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🛒 Подтвердить возврат заказа в продажу', callback_data=Product_cb(idx=idx, action='confirm_back_order').pack())], 
        [InlineKeyboardButton(text='👈 Назад', callback_data=Product_cb(idx=idx, action='back').pack())]
        ]))


# Обработка возвращения товара в продажу
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'confirm_back_order'))
async def order_confirm(query: CallbackQuery, callback_data: Product_cb):
    idx = callback_data.idx
    await query.message.delete()

    data_order = await db.fetchone('SELECT * FROM orders WHERE idx = ?', (idx,))

    # Добавляем товар обратно в продажу
    print(data_order)
    title = data_order[2]
    body = data_order[3]
    photo = data_order[4]
    price = data_order[5]
    pay_link = data_order[6]

    await db.query('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', (idx, title, body, photo, price, pay_link))

    await db.query('DELETE FROM orders WHERE idx = ?', (idx,))



    await query.message.answer(text='✅ ЗАКАЗ ВЫПОЛНЕН ✅')