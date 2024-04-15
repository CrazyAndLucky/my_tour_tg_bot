from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BufferedInputFile, CallbackQuery, ReplyKeyboardRemove, LinkPreviewOptions, MessageEntity
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from hashlib import md5

from loader import dp, db, bot
from shop_bot.filters import IsAdmin
from shop_bot.keyboards.default.markups import accounts, orders, add_account, admins, mailling
from shop_bot.states import ProductState, Add_admin_state, Del_admin_state, Mailling_state
# from shop_bot.app import cmd_start


main_admin_id = 1366711027


# Выводит список админов
@dp.message(IsAdmin(), (F.text == admins))
async def process_setting_admin(message: Message, state: FSMContext):
    text_admins = '<b>АДМИНЫ</b>\n\n' # Сообщение со списком админов
    
    # Достаем из базы админов и формируем сообщение
    for admin_id in await db.fetchall('SELECT * FROM admins'):
        admin = await bot.get_chat(admin_id[0])
        
        text_admins += f'{admin.first_name} {admin.id}\n'
    
    
    await message.answer(text=text_admins, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить админа', callback_data='add_admin')],
        [InlineKeyboardButton(text='➖ Удалить админа', callback_data='del_admin')]
        ]))


# Добавление нового админа
@dp.callback_query(IsAdmin(), (F.data == 'add_admin'))
async def process_add_admin(query: CallbackQuery, state: FSMContext):
    await state.set_state(Add_admin_state.name)
    await query.message.answer(text='Введи ид')


# Сохранение нового админа
@dp.message(IsAdmin(), Add_admin_state.name)
async def process_save_admin(message: Message, state: FSMContext):
    try:
        usr_id = (await bot.get_chat(chat_id=int(message.text))).id
        
        # Сохраняем админа
        await db.query('DELETE FROM users WHERE cid = ?', (usr_id,))
        await db.query('INSERT INTO admins VALUES (?)', (usr_id,))
        await state.clear() # Очищаем статус

        await message.answer(text='Добавлен новый админ')
        
        await bot.send_message(chat_id=usr_id, text='⭐️ Поздравляю! Ты теперь админ! <b>Обязательно перезапусти бота, чтобы появилсь новые функции</b>')
        
    except Exception:
        await message.answer('Такого пользователя не найдено')


# Удаление админа
@dp.callback_query(IsAdmin(), (F.data == 'del_admin'))
async def process_del_admin(query: CallbackQuery, state: FSMContext):
    await state.set_state(Del_admin_state.name)
    await query.message.answer(text='Введи ид')

# Сохраняем удленного админа
@dp.message(IsAdmin(), Del_admin_state.name)
async def process_save_admin(message: Message, state: FSMContext):
    try:
        usr_id = (await bot.get_chat(chat_id=int(message.text))).id
        
        # Удаляем админа
        await db.query('DELETE FROM admins WHERE cid = ?', (usr_id,))
        await db.query('INSERT INTO users VALUES (?, 1)', (usr_id,))
        await state.clear()

        await message.answer(text='Админ разжалован')
        # await cmd_start(message, state)
        
    except Exception:
        await message.answer('Такого пользователя не найдено')



# Рассылка
@dp.message(IsAdmin(), (F.text == mailling))
async def process_mailling(message: Message):
    # Достаем активных пользователей
    active_users = await db.fetchall('SELECT cid FROM users WHERE status = 1')
    len_active_users = len(active_users)
    # Достаем пользователей которые заблокировали бота
    non_users = active_users = await db.fetchall('SELECT cid FROM users WHERE status = 0')
    len_non_users = len(non_users)

    await message.answer(
        text=f'❕Всего пользователей в боте - {len_active_users + len_non_users}\n❕Активных - {len_active_users}\n❕В блоке - {len_non_users}',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Сделать рассылку', callback_data='add_mailling')]])
        )
    
# Попросить сообщение для рассылки
@dp.callback_query(IsAdmin(), (F.data == 'add_mailling'))
async def add_message(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text='Отправь сообщение для рассылки')
    
    await state.set_state(Mailling_state.message)


# Добавление сообщения и подтверждение рассылки
@dp.message(IsAdmin(), Mailling_state.message)
async def process_save_admin(message: Message, state: FSMContext):
    await message.answer(text='⬇️ СООБЩЕНИЕ ДЛЯ РАССЫЛКИ ⬇️')
    await message.answer(
        text=message.text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='☑️ Начать рассылку', callback_data='confirm_mailling')],
            [InlineKeyboardButton(text='🚫 Отмена', callback_data='stop_mailling')]
            ]),
        entities=message.entities,
        parse_mode=None
        )
    
    # Сохраняем сообщения для рассылки
    await state.update_data(text=message.text)
    await state.update_data(entities=message.entities) # Сохраняем разсетаку и кастомные эмодзи


# Старт рассылки
@dp.callback_query(IsAdmin(), (F.data == 'confirm_mailling'))
async def start_mailling(query: CallbackQuery, state: FSMContext):
    # Достаем активных пользователей
    active_users = await db.fetchall('SELECT cid FROM users WHERE status = 1')
    
    await query.message.delete()

    await query.message.answer(text='Рассылка началась')
    
    # Достаем сообщения для рассылки
    data: dict = await state.get_data()
    await state.clear()

    text_mailling = data['text']
    # Разметка текста
    entities = data['entities']

    # Бежим по всем пользователям бота и отправляем сообщение, а если не получается обновляем данные в базе
    sending = []
    for active_user in active_users:
        try:
            await bot.send_message(
                chat_id=active_user[0], 
                text=text_mailling, 
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                entities=entities,
                parse_mode=None
                )
            sending.append(active_user[0])
        except Exception as e:
            await db.query('UPDATE users SET status = 0')
        
    # Пишем отчет
    len_sending = len(sending)
    await query.message.answer(
        text=f'✅ РАССЫЛКА ЗАВЕРШЕНА ✅\n\nСообщений отправленно - {len_sending}'
    )


# Отмена рассылки
@dp.callback_query(IsAdmin(), (F.data == 'stop_mailling'))
async def stop_mailling(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.clear()

    # Возвращаемся в начало
    await process_mailling(query.message)