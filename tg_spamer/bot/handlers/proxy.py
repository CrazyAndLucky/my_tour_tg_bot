from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, db
from tg_spamer.tools import proxy_manager
from tg_spamer.clients import clients_list, update_clients_list


class MyForm(StatesGroup):
    await_proxy_http = State()
    await_proxy_socks5 = State()


class MyCallback(CallbackData, prefix='proxy_type'):
    proxy_type: str
    

@dp.callback_query(F.data == 'info_proxy')
async def info_proxy(query: CallbackQuery, state: FSMContext):
    all_proxy = proxy_manager.get_all_proxy()
    
    text = ''
    for one_proxy in all_proxy:
        text += one_proxy
        text += '\n'

    builder = InlineKeyboardBuilder()
    if all_proxy:
        builder.button(text='🔛 Распредилить прокси', callback_data='give_proxy')
        builder.button(text='➕ Добавить прокси', callback_data='add_proxy')
        builder.button(text='🗑 Удалить прокси', callback_data='dell_proxy')
    else:
        builder.button(text='➕ Добавить прокси', callback_data='add_proxy')    
    
    builder.button(text='👈 Назад', callback_data='spam_settings')
    builder.adjust(1)

    try:
        await query.message.edit_text(
            text=f'Свободные прокси:\n{text}', 
            reply_markup=builder.as_markup()
            )
    except Exception:
        pass
    

# Удалить прокси из базы
@dp.callback_query(F.data == 'dell_proxy')
async def dell_proxy(query: CallbackQuery, state: FSMContext):
    proxy_manager.delete_all_proxy()
    await info_proxy(query, state)


# Добавить прокси в базу, по умолчанию http
@dp.callback_query(F.data == 'add_proxy')
@dp.callback_query(MyCallback.filter(F.proxy_type == 'http'))
async def add_proxy_http(query: CallbackQuery, state: FSMContext):
    await state.set_state(MyForm.await_proxy_http)

    await query.message.edit_text(
        text='Отправьте список прокси в чат как сообщение. \nПрокси в формате: login:password@host:port',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='http', callback_data=MyCallback(proxy_type='socks5').pack())],
            [InlineKeyboardButton(text='👈 Назад', callback_data='info_proxy')],
        ])
        )
    

# Меняем тип проски на socks5
@dp.callback_query(MyCallback.filter(F.proxy_type == 'socks5'))
async def add_proxy(query: CallbackQuery, state: FSMContext):
    await state.set_state(MyForm.await_proxy_socks5)

    await query.message.edit_text(
        text='Отправьте список прокси в чат как сообщение. \nПрокси в формате: host:port:login:password',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='socks5', callback_data=MyCallback(proxy_type='http').pack())],
            [InlineKeyboardButton(text='👈 Назад', callback_data='info_proxy')],
        ])
        )
    

# Сохранение прокси в базе http
@dp.message(MyForm.await_proxy_http)
async def proxy_http_save(message: Message, state: FSMContext):
    await message.delete()
    message_split = message.text.strip().split('\n')

    for message_proxy in message_split:
        proxy = 'http:'
        proxy += message_proxy.strip()
        proxy_manager.insert_proxy(proxy)


# Сохранение прокси в базе socks5
@dp.message(MyForm.await_proxy_socks5)
async def proxy_socks_save(message: Message, state: FSMContext):
    await message.delete()
    message_split = message.text.strip().split('\n')

    for message_proxy in message_split:
        proxy = 'socks5:'
        proxy += message_proxy.strip()
        proxy_manager.insert_proxy(proxy)


# Распределить проски среди аккаунтов без прокси
@dp.callback_query(F.data == 'give_proxy')
async def give_proxy(query: CallbackQuery, state: FSMContext):
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('нет прокси',))

    if accounts: # Если есть аккаунты без проски, бежим по ним 
    #     for account in accounts:
    #         proxy_str = proxy_manager.get_one_proxy() # Пытаемся достать из базы прокси
    #         if proxy_str is not None: 
    #             proxy = proxy_manager.pars_proxy(proxy_str)
    #             db.query('UPDATE accounts SET proxy = ?, status = ? WHERE unique_id = ?', (str(proxy), 'новый', account[0]))
    #         else:
    #             await query.answer('Не хватает прокси', show_alert=True)
        
        # Обновляем список клиентов
        await update_clients_list(distribute_proxies=True)
        await info_proxy(query, state)

    else:
        await query.answer('У всех аккаунтов есть прокси', show_alert=True)