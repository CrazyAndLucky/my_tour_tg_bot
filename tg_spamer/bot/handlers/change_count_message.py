from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, bot
from tg_spamer.clients import update_clients_list, accounts_manager, config
from tg_spamer.tools import numbers_in_emoji




class MyForm(StatesGroup):
    await_accounts_numbers_msg = State()
    await_count_msg = State()

class MyCallback(CallbackData, prefix='status'):
    action: str
    status: str


# Изменение пличества доступных сообщений для аккаунта
@dp.callback_query(F.data == 'change_count_message')
async def status_accounts_settings(query: CallbackQuery, state: FSMContext):
    # Достали из базы аккаунты
    new_accounts = accounts_manager.get_all_acc_info_by_status('новый')
    prep_accounts = accounts_manager.get_all_acc_info_by_status('прогрев')
    ready_accounts = accounts_manager.get_all_acc_info_by_status('готов')
    after_spam_accounts = accounts_manager.get_all_acc_info_by_status('отлежка')
    spam_block_accounts = accounts_manager.get_all_acc_info_by_status('спам')
    no_proxy_accounts = accounts_manager.get_all_acc_info_by_status('нет прокси')

    # Присваиваем порядковые номера и аккаунтам и формируем строку
    text = 'Введите номера аккаунтов через пробел для редактирования (3 6 7), можно ввести диапазон (5-10)'
    number = 0
    all_accounts = []

    text += '\n\n<b>НОВЫЕ</b>\n'
    for account in new_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]}\n'

    text += '\n<b>ПРОГРЕВ</b>\n'
    for account in prep_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]} сообщения | {account[6]} |\n'

    text += '\n<b>ГОТОВ</b>\n'
    for account in ready_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]} сообщения | {account[6]} |\n'

    text += '\n<b>ОТЛЕЖКА</b>\n'
    for account in after_spam_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]} сообщения | {account[6]} |\n'

    text += '\n<b>СПАМ</b>\n'
    for account in spam_block_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]} сообщения | {account[6]} |\n'

    text += '\n<b>НЕТ ПРОКСИ</b>\n'
    for account in no_proxy_accounts:
        all_accounts.append(account[0])
        number += 1
        text += numbers_in_emoji(number)
        text += f' {account[0]} сообщения | {account[6]} |\n'


    # Сохраняем в состоянии все аккаунты для дальнейшего использования 
    await state.set_state(MyForm.await_accounts_numbers_msg)
    await state.update_data(all_accounts=all_accounts)    
    await query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👈 Назад', callback_data='spam_settings')]
        ])
    )


# Получаем аккаунты для редактирования
@dp.message(MyForm.await_accounts_numbers_msg)
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
    text += '\n\nВведите кол-во сообщений на аккаунт'
    await state.set_state(MyForm.await_count_msg)

    # Сохранить в статус аккаунты для редактирования для дальнейшего использования
    await state.update_data(edit_accounts=edit_accounts)

    await message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👈 Назад', callback_data='change_count_message')]
        ]) 
        )
    

# Получаем кол-во сообщений на аккаунт
@dp.message(MyForm.await_count_msg)
async def count_msg(message: Message, state: FSMContext):
    edit_accounts = (await state.get_data())['edit_accounts']
    for unique_id in edit_accounts:
        config._update_msg(unique_id=unique_id, value=int(message.text))
    
    await message.answer(
        text='Поменял кол-во сообщений',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Продолжить', callback_data='spam_settings')]
        ])                             
    )