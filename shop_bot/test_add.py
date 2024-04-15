from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from hashlib import md5

from loader import dp, db, bot
from filters import IsAdmin, MyFilter
from states import CategoryState, ProductState
from keyboards import back_markup


cancel_message = '🚫 Отменить'
add_product = '➕ Добавить товар'
delete_category = '🗑️ Удалить категорию'
back_message = '👈 Назад'
all_right_message = '✅ Все верно'
back_category_list_message = '👈 К списку категорий'
settings = 'Настройки категории'

# Собственные возвращаемые данные категории
class Category_cb(CallbackData, prefix='category'):
    id: str
    action: str

# Данные продуктов
class Product_cb(CallbackData, prefix='product'):
    id: str
    action: str


# Отображение списка категрий
@dp.message(IsAdmin(), MyFilter(settings))
async def process_settings(message: Message):
    builder = InlineKeyboardBuilder()

    for idx, title in db.fetchall('SELECT * FROM categories'):
        builder.button(text=title, callback_data=Category_cb(id=idx, action='view'))

    builder.add(InlineKeyboardButton(
        text='+ Добавить категорию', 
        callback_data='add_category'
        ))
    
    builder.adjust(1) # Расположить кнопки вертикально
    await message.answer(text='Настройка категорий', reply_markup=builder.as_markup())


# Добавление категории
@dp.callback_query(IsAdmin(), F.data == 'add_category')
async def add_category_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text='Название категории?')
    await state.set_state(CategoryState.title)


# Ввод названия категории и обоновление в базе
@dp.message(IsAdmin(), CategoryState.title)
async def set_category_title_handler(message: Message, state: FSMContext):
    category = message.text
    idx = md5(category.encode('utf-8')).hexdigest() # Хэширование id
    db.query('INSERT INTO categories VALUES (?, ?)', (idx, category)) 

    # Выводим обновленную категорию
    await state.clear()
    await process_settings(message)


# Отображение товаров в категории
@dp.callback_query(IsAdmin(), Category_cb.filter(F.action == 'view'))
async def category_callback_handler(
    query: CallbackQuery,
    callback_data: Category_cb,
    state: FSMContext,
    ):
    category_idx = callback_data.id

    products = db.fetchall(
        '''SELECT * FROM products product WHERE product.tag = 
        (SELECT title FROM categories WHERE idx=?)''',
        (category_idx,)
    )

    await query.message.delete()
    await query.message.answer('Все добавленные товары в эту категорию')
    await state.update_data(category_index=category_idx) # Обновляем статус
    await show_products(query.message, products, category_idx) # Отображаем продукты


# Отображение товаров в категории
async def show_products(message: Message, product, category_idx):
    await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
    
    # Отправить каждый товар
    for idx, title, body, image, price, tag in product:
        text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price} рублей.'

        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🗑️ Удалить', callback_data=Product_cb(id=idx, action='delete').pack())]])

        await message.answer_photo(photo=BufferedInputFile(image, filename='image'), caption=text, reply_markup=markup)

    # Добавление товара и удаление категории
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=add_product), KeyboardButton(text=delete_category)], [KeyboardButton(text=back_category_list_message)]], 
        resize_keyboard=True,
        )
    
    await message.answer(
        'Хотите что-нибудь добавить или удалить?', 
        reply_markup=markup
        )

# Возврат к списку категорий из списка товаров
@dp.message(IsAdmin(), F.text == back_category_list_message)
async def back_category_list_handler(message: Message):
    await process_settings(message)


# Удаление категории
@dp.message(IsAdmin(), F.text == delete_category)
async def delete_category_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'category_index' in data.keys():
        idx = data['category_index']

        # Удаление товаров из базы
        db.query(
            '''DELETE FROM products WHERE tag IN (SELECT title FROM categories
            WHERE idx=?)''', (idx,)
        )

        # Удаелиние кегории
        db.query('DELETE FROM categories WHERE idx=?', (idx,))

        # Удаление клавиатуры и отображение оставшихся категорий
        await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
        await process_settings(message)


# Добавление товара
@dp.message(IsAdmin(), F.text == add_product)
async def process_add_product(message: Message, state: FSMContext):
    await state.set_state(ProductState.title) # Состояние ввода названия товара

    # Кнопка для отмены
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=cancel_message)]], resize_keyboard=True)

    await message.answer('Введите название товара', reply_markup=markup)


# Отмена создания товара
@dp.message(IsAdmin(), F.text == cancel_message, ProductState.title)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Ок, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.clear()

    await process_settings(message)


# Добавление названия
@dp.message(IsAdmin(), ProductState.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text) # Запоминаем название
    await state.set_state(ProductState.body) # Меняем состояние

    await message.answer('Введите описание', reply_markup=back_markup())

# Возврат к созданию описания товара 
@dp.message(IsAdmin(), F.text == back_message)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message, state=state)


# Добавление описания
@dp.message(IsAdmin(), ProductState.body)
async def process_body(message: Message, state: FSMContext):
    await state.update_data(body=message.text) # Сохраняем описание
    await state.set_state(ProductState.image) # Следующее состояние

    await message.answer(text='Отправьте фото', reply_markup=back_markup())


# Добавление фото
@dp.message(IsAdmin(), ProductState.image, F.photo)
async def process_image_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id # [-1] Изображение в лучшем разрешении
    file_info = await bot.get_file(file_id=file_id) # Для получения ссылки на скачивание

    downloaded_file = (await bot.download_file(file_path=file_info.file_path)).read() # Файл в бинарном режиме

    await state.update_data(image=downloaded_file)

    await state.set_state(ProductState.price)
    await message.answer(text='Цена?', reply_markup=back_markup())
    

# Цена и подтверждение
@dp.message(IsAdmin(), ProductState.price, F.text.isdigit())
async def process_price(message: Message, state: FSMContext):
    data = await state.get_data() # Загружаем данные о товаре из состояния
    price = data['price'] = message.text # Добавляем цену в данные
    await state.update_data(price=price)
    await state.set_state(ProductState.confirm)

    title = data['title']
    body = data['body']
    image = data['image']

    text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price} рублей'

    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=back_message), KeyboardButton(text=all_right_message)]], resize_keyboard=True)

    await message.answer_photo(photo=BufferedInputFile(image, filename='image'), caption=text, reply_markup=markup)


# Добавление товара в базу
@dp.message(IsAdmin(), ProductState.confirm, F.text == all_right_message)
async def process_confirm(message: Message, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    title = data['title']
    body = data['body']
    image = data['image']
    price = data['price']


    await state.clear() # Очиста состояния

    tag = db.fetchall(
        'SELECT title FROM categories WHERE idx=?', (data['category_index'],)
    )[0][0] # Функция возвращает картеж, получаем занечение из него

    idx = md5(''.join([title, body, price, tag]
                      ).encode()).hexdigest() # Хэшируем

    db.query(
        'INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', 
        (idx, title, body, image, int(price), tag,)
        )

    await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
    await process_settings(message)


# Удаление продукта
@dp.callback_query(IsAdmin(), Product_cb.filter(F.action == 'delete'))
async def delete_product_callback_handler(query: CallbackQuery, callback_data: Product_cb):
    product_idx = callback_data.id # id из callback

    db.query('DELETE FROM products WHERE idx=?', (product_idx,))

    await query.message.answer(text='Удалено!')
    await query.message.delete()