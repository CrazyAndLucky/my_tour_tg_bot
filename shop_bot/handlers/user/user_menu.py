from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BufferedInputFile, CallbackQuery
from aiogram import F
from aiogram.filters.callback_data import CallbackData

from shop_bot.filters import IsUser
from shop_bot.keyboards.default.markups import accounts, back_message, confirm_message, reviews, reference, help_button, orders
from shop_bot.keyboards import confirm_markup, menu_user_markup, back_markup
from loader import db, dp, bot


id_notification = 1366711027

reviews_message = '♻️ Канал с отзывами - @...\n✅ Основной канал - @...'
reference_message = '''
<b>КАК ПРОИСХОДИТ ПРОЦЕСС ПОКУПКИ</b>

🔶 Вы выбираете в каталоге това и оплачиваете его.
🔶 После этого ваш заказ поступает в работу, пожалуйста, будьте терпеливы так как все заказы обрабатываются в ручную.
...
'''
help_message = '💎 Обратная связь, по всем вопросам - @...'


class Product_cb(CallbackData, prefix='product'):
    idx: str
    action: str

class Pay_cb(CallbackData, prefix='pay'):
    idx: str
    action: str


# Отображаем для пользователя аккаунты в продаже
@dp.message(IsUser(), F.text == accounts)
async def process_user_account_show(message: Message):
    # Достаем список активных заказов из базы
    accounts = await db.fetchall('SELECT * FROM products')

    # Если аккаунты есть в продаже
    if len(accounts) != 0:
        await message.answer(text='<b>🔽ТОВАРЫ В ПРОДАЖЕ🔽</b>')

        for idx, _, body, photo, price, _ in accounts:
            text = f'{price}руб.\n\n{body}'

            await message.answer_photo(
                photo=BufferedInputFile(file=photo, filename='image'),
                caption=text, 
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить', callback_data=Product_cb(idx=idx, action='buy_account').pack())]]),
                )
    else:
        await message.answer(text='☹️ Здесь пока пусто, попробуй запустить позже')
            

# Нажал на покупку
@dp.callback_query(IsUser(), Product_cb.filter(F.action == 'buy_account'))
async def process_buy_account(query: CallbackQuery, callback_data: Product_cb):      
    await query.message.delete()
    idx = callback_data.idx

    account = await db.fetchone('SELECT * FROM products WHERE idx = ?', (idx,))
    
    # Если аккаунта уже нет в продаже
    if len(account) != 0:
        body = account[2]
        photo = account[3]
        price = account[4]
        
        text = f'{price}\n\n{body}'

        await query.message.answer_photo(
            photo=BufferedInputFile(file=photo, filename='image'),
            caption=text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Оплатить', callback_data=Pay_cb(idx=idx, action='pay_link').pack())],
                    ]
                ))
    
    else:
        await query.message.answer(text='Этого аккаунта уже нет в продаже')
        await query.message.delete()


# Получение ссылки на оплату
@dp.callback_query(IsUser(), Pay_cb.filter(F.action == 'pay_link'))
async def process_get_linc(query: CallbackQuery, callback_data: Pay_cb):
    idx = callback_data.idx
    
    await query.message.answer(text=f'Привет! держи ссылку на оплату: https/...\n\n' + 
                            '<b>После совершения оплаты не забудь нажать кнопку "✅ Подтвердить оплату" Тогда твой заказ поступит в работу.</b>\n\n',
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='🔗 Ссылка на оплату', callback_data='1')],
                                [InlineKeyboardButton(text='✅ Подтвердить оплату',callback_data=Product_cb(idx=idx, action='pay').pack())]
                                ])
                            )


# Пользователь подтвердил оплату
@dp.callback_query(IsUser(), Product_cb.filter(F.action == 'pay'))
async def process_pay(query: CallbackQuery, callback_data: Product_cb):
    await query.message.answer(text='Заказ поступил в работу, скоро с вами свяжется админ: @...')
    idx = callback_data.idx
    # Достаю аккаунт из базы
    account = await db.fetchone('SELECT * FROM products WHERE idx = ?', (idx,))
    
    title = account[1]
    body = account[2]
    photo = account[3]
    price = account[4]
    pay_link = account[5]

    # Добавляем запись в заказы
    await db.query(
        'INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)', 
        (query.message.chat.id, idx, title, body, photo, price, pay_link)
        )
    
        # Удаляем из доступных аккаунтов к покупки
    await db.query('DELETE FROM products WHERE idx = ?', (idx,))

    
    # Оповещение для админов
    admins = await db.fetchall('SELECT * FROM admins')
    for admin in admins:
        await bot.send_message(chat_id=admin[0], text='<b>ПОСТУПИЛ НОВЫЙ ЗАКАЗ</b>')



# # Отмена подтверждения
# @dp.message(IsUser(), F.text == back_message)
# async def back_account(message: Message):
#     await message.answer(text='Отмена', reply_markup=menu_user_markup())

#     await process_user_account_show(message)

# # Подтверждение покупки
# @dp.message(IsUser(), F.text == confirm_message)
# async def confirm_account(message: Message):
#     pass


# Кнопка канал с отзывами
@dp.message(IsUser(), F.text == reviews)
async def reviews_button(message: Message):
    await message.answer(text=reviews_message)


# Кнопка справка
@dp.message(IsUser(), F.text == reference)
async def reference_button(message: Message):
    await message.answer(text=reference_message)


# Кнопка помощь
@dp.message(IsUser(), F.text == help_button)
async def reference_button(message: Message):
    await message.answer(text=help_message)


# Отображение активных заказов у пользователя
@dp.message(IsUser(), F.text == orders)
async def orders_button(message: Message):
    usr_orders = await db.fetchall('SELECT * FROM orders WHERE cid = ?', (message.chat.id,))
    if len(usr_orders) == 0:
        await message.answer('У вас пока нет заказов :(')
    else:

        for usr_order in usr_orders:
            body = usr_order[3]
            photo = usr_order[4]
            price = usr_order[5]
            
            text = f'{price}руб.\n\n{body}\n\n<b>Заказ находится в работе, его вам выдаест @...</b>'           

            await message.answer_photo(
                photo=BufferedInputFile(file=photo, filename='image'),
                caption=text
                )