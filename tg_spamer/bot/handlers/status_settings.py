import os
import shutil
from zipfile import ZipFile
from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, bot
from tg_spamer.clients import update_clients_list, accounts_manager
from tg_spamer.tools import numbers_in_emoji



class MyForm(StatesGroup):
    await_accounts_numbers = State()

class MyCallback(CallbackData, prefix='status'):
    action: str
    status: str


@dp.callback_query(F.data == 'status_accounts_settings')
async def status_accounts_settings(query: CallbackQuery, state: FSMContext):
    new_accounts = accounts_manager.get_unique_id_by_status('новый')
    prep_accounts = accounts_manager.get_unique_id_by_status('прогрев')
    ready_accounts = accounts_manager.get_unique_id_by_status('готов')
    after_spam_accounts = accounts_manager.get_unique_id_by_status('отлежка')
    spam_block_accounts = accounts_manager.get_unique_id_by_status('спам')
    no_proxy_accounts = accounts_manager.get_unique_id_by_status('нет прокси')

    # Присваиваем порядковые номера аккаунтам и формируем строку
    text = 'Введите номера аккаунтов через пробел для редактирования (3 6 7), можно ввести диапазон (5-10)'
    number = 0
    all_accounts = []

    text += '\n\n<b>НОВЫЕ</b>\n'
    for account in new_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'

    text += '\n<b>ПРОГРЕВ</b>\n'
    for account in prep_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'

    text += '\n<b>ГОТОВ</b>\n'
    for account in ready_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'

    text += '\n<b>ОТЛЕЖКА</b>\n'
    for account in after_spam_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'

    text += '\n<b>СПАМ</b>\n'
    for account in spam_block_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'

    text += '\n<b>НЕТ ПРОКСИ</b>\n'
    for account in no_proxy_accounts:
        all_accounts.append(account)
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account}\n'


    # Сохраняем в состоянии все аккаунты для дальнейшего использования 
    await state.set_state(MyForm.await_accounts_numbers)
    await state.update_data(all_accounts=all_accounts)    
    await query.message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👈 Назад', callback_data='back')]
        ])
    )



@dp.message(MyForm.await_accounts_numbers)
async def proccess_take_numbers(message: Message, state: FSMContext):
    await message.delete()
    
    text = message.text
    # Достаем из состояние все аккаунты
    all_accounts = (await state.get_data())['all_accounts']
    
    edit_accounts = []
    if '-' in text:
        text_split = text.strip().split('-')
        try:
            number_1 = int(text_split[0])
            number_2 = int(text_split[1])
        
            edit_accounts = all_accounts[number_1 - 1:number_2]
        except Exception:
            pass

    else: 
        text_split = text.strip().split(' ')
        
        for acc_index in text_split:
            try:
                edit_accounts.append(all_accounts[int(acc_index) - 1])
            except Exception:
                pass


    text = '<b>Выбранны аккаунты:</b>\n'
    for acc in edit_accounts:
        text += f'{acc}\n'
    
    # Сохранить в статус аккаунты для редактирования для дальнейшего использования
    await state.update_data(edit_accounts=edit_accounts)

    await message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👇 ПОМЕНЯТЬ СТАТУС НА 👇', callback_data='none')],
            [
                InlineKeyboardButton(text='новый', callback_data=MyCallback(action='change_status', status='новый').pack()), 
                InlineKeyboardButton(text='прогрев', callback_data=MyCallback(action='change_status', status='прогрев').pack()),
                InlineKeyboardButton(text='готов', callback_data=MyCallback(action='change_status', status='готов').pack()), 
                ],
            [
                InlineKeyboardButton(text='отлежка', callback_data=MyCallback(action='change_status', status='отлежка').pack()), 
                InlineKeyboardButton(text='спам', callback_data=MyCallback(action='change_status', status='спам').pack()),
                InlineKeyboardButton(text='нет прокси', callback_data=MyCallback(action='change_status', status='нет прокси').pack()),
                ],
            [InlineKeyboardButton(text='👈 Назад', callback_data='status_accounts_settings')],
        ]))
    

@dp.callback_query(MyCallback.filter(F.action == 'change_status'))
async def change_on_new(query: CallbackQuery, state: FSMContext, callback_data: MyCallback):    
    # Достаем из состояние все аккаунты
    edit_accounts = (await state.get_data())['edit_accounts']
    status = callback_data.status

    text = 'Статус аккаунтов изменен:\n'
    for unique_id in edit_accounts:
        if status == 'прогрев':
            accounts_manager.post_acc(unique_id=unique_id, status=status, time=datetime.now())
        else:
            accounts_manager.post_acc(unique_id=unique_id, status=status)
        text += f'{unique_id}\n'

    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Продолжить', callback_data='tg_spamer')]
        ])
    )