from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BufferedInputFile, CallbackQuery, ReplyKeyboardRemove
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from hashlib import md5

from loader import dp, db, bot
from shop_bot.filters import IsAdmin
from shop_bot.keyboards.default.markups import accounts, orders, add_account, admins, mailling
from shop_bot.states import ProductState, Add_admin_state


delete_product = 'Удалить'

class Product_cb(CallbackData, prefix='product'):
    idx: str
    action: str


# Отображаем для админа аккаунтов в продаже
@dp.message(IsAdmin(), F.text == accounts)
async def process_admin_account_show(message: Message, state: FSMContext):
    # Очичаем состояние, если в нем были
    await state.clear()

    await message.answer(text='<b>🔽 ТОВАРЫ В ПРОДАЖЕ 🔽</b>')

    for idx, title, body, photo, price, _ in await db.fetchall('SELECT * FROM products'):
        text = f'{title}\n\n{price} руб.\n\n{body}'

        await message.answer_photo(
            photo=BufferedInputFile(file=photo, filename='image'),
            caption=text, 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=delete_product, callback_data=Product_cb(idx=idx, action='delete_product').pack())]]),
            )

    # Сообщеине и клавиатура с добавлением аккаунтов в продажу
    await message.answer(
        text='🔼 <b>ТОВАРЫ В ПРОДАЖЕ</b> 🔼',
        reply_markup=(InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=add_account, callback_data='add_product')]]))
        )

# Удалить товар
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'delete_product'))
async def process_delete_product(query: CallbackQuery, callback_data: Product_cb):
    await db.query('DELETE FROM products WHERE idx = ?', (callback_data.idx,))

    await query.message.delete()


# Заметка для аккаунта
@dp.callback_query(IsAdmin(), F.data == 'add_product')
async def process_add_product(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Введите заметку для товара (пользователь не будет видеть этих данных, эти данные нужны для верификации товара)')
    await state.set_state(ProductState.title)


# Сохраняем название и предлагаем ввести цену
@dp.message(IsAdmin(), ProductState.title)
async def product_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(ProductState.price)
    await message.answer(text='Цена?')


# Сохраняем цену и предлагаем ввести описание
@dp.message(IsAdmin(), ProductState.price, F.text.isdigit())
async def product_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(ProductState.body)
    await message.answer(text='Описание?')


# Сохраняем описание и предлагаем отправить фото
@dp.message(IsAdmin(), ProductState.body)
async def product_price(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(ProductState.image)
    await message.answer(text='Фото?')


# Сохраняем фото и предлагаем ввести ссылку для оплаты
@dp.message(IsAdmin(), ProductState.image, F.photo)
async def product_price(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id # [-1] Изображение в лучшем разрешении

    # Скачиваем фото и представляем его в байтах
    image = (await bot.download(file=file_id)).read() 
    
    data = await state.get_data() # Получаем данные из состояние
    await state.clear() # Обнуляем состояние

    title = data['title']
    price = data['price']
    body = data['body']

    idx = md5(''.join([title, price, body]).encode()).hexdigest()

    # Сохраняем товар в базу
    await db.query('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', (idx, title, body, image, price, 'pay_link'))

    await process_admin_account_show(message, state)



