import os

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, Message, LinkPreviewOptions
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, bot
from tg_spamer.functions import spam_message_button
from tg_spamer.clients import config, links_manager, accounts_manager



class MyForm(StatesGroup, prefix='links'):
    link = State()

class MyCallback(CallbackData, prefix='spam_biutton'):
    spam: str
    action: str



# Настройки 
@dp.callback_query(F.data == 'button_spam_settings')
async def button_spam_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    links = links_manager.get_all_links()

    if links:
        markup =  InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='▶️ Начать рассылку', callback_data='choice_spam_button')],
            [InlineKeyboardButton(text='➕ Добавить ссылку', callback_data='add_linck')],
            [InlineKeyboardButton(text='🗑 Удалить все сслыки', callback_data='dell_lincks')],
            [InlineKeyboardButton(text='👈 Назад', callback_data='back')],
        ])
    
    else: 
        markup =  InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='➕ Добавить ссылку', callback_data='add_linck')],
            [InlineKeyboardButton(text='🗑 Удалить все сслыки', callback_data='dell_lincks')],
            [InlineKeyboardButton(text='👈 Назад', callback_data='back')],
        ])
    

    text = '<b>Доступные сообещния с кнопками:</b>\n'
    for link in links:
        text += f'{link[1]}{link[2]} кол-во сообщений: {link[3]}\n'

    await query.message.edit_text(
        text=text,
        reply_markup=markup,
        link_preview_options=LinkPreviewOptions(is_disabled=True)
        )
    


# Выбор типа рассылки
@dp.callback_query(F.data == 'choice_spam_button')
async def choice_spam_button(query : CallbackQuery, state: FSMContext):
    accounts = accounts_manager.get_all_acc_info_by_status('готов')
    if accounts:
        text = '<b>⬇️РАССЫЛКА СООБЩЕНИЯ С КНОПКОЙ⬇️</b>\n'
        for account in accounts:
            text += f'| {account[0]} | доступно сообщений | {account[6]} |\n'


        dual_message = config.dual_message()
        if dual_message == 1:
            text += '\nДвойная отправка: ✅'
        else:
            text += '\nДвойная отправка: ❌'

        await query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🤖 Рассылка через PostBot', callback_data=MyCallback(spam='confirm_spam_button', action='postbot').pack())],
                [InlineKeyboardButton(text='👈 Назад', callback_data='button_spam_settings')],
            ])
        )

    else: 
        await query.answer(text='Нет готовых аккаунтов к рассылке', show_alert=True)


# Подтверждение рассылки
@dp.callback_query(MyCallback.filter(F.spam == 'confirm_spam_button'))
async def confirm_spam_button(query: CallbackQuery, state: FSMContext, callback_data: MyCallback):
    if callback_data.action == 'link':
        text = 'Начать расслку через перессылание сообщения с канала?'
        callback = MyCallback(spam='start_spam_button', action='link').pack()
    else: 
        text = 'Начать расслку через PostBot?'
        callback = MyCallback(spam='start_spam_button', action='postbot').pack()


    await query.message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='✅ Начать', callback_data=callback)],
                [InlineKeyboardButton(text='👈 Назад', callback_data='choice_spam_button')],
            ])
        )


# Начать рассылку
@dp.callback_query(MyCallback.filter(F.spam == 'start_spam_button'))
async def start_spam_button(query: CallbackQuery, state: FSMContext, callback_data: MyCallback):
    # config.clear_log_file()
    dual_send = config.dual_message()

    # Сохраняю те аккаунты, которые будут в рассылке
    spam_accounts = accounts_manager.get_unique_id_by_status(status='готов')

    await query.message.edit_text(text='Начинаю рассылку')
    if callback_data.action == 'link':
        await spam_message_button([query.from_user.username,], dual_send)
    else:
        await spam_message_button([query.from_user.username,], dual_send, postbot=True)

    # После завершения подсчитываю кол-во отправленных сообщений аккаунтом
    text = f'<b>Завершил рассылку</b> | {config.get_count_send_msg()} |\n'
    for spam_account in spam_accounts:
        account_info = accounts_manager.get_acc_info_by_unique_id(spam_account)
        if account_info is None:
            text += '<i>Забанен</i>\n'
        else:
            text += f'<i>{spam_account}</i> - | {account_info[7]} |\n'

    # await query.message.answer(text=text)
    await query.message.answer_document(document=FSInputFile(path='tg_spamer/logs.txt'), caption=text)



# Добавить ссылку
@dp.callback_query(F.data == 'add_linck')
async def add_linck(query: CallbackQuery, state: FSMContext):
    await state.set_state(MyForm.link)

    await query.message.edit_text(
        text='Отправьте ссылку на пост из бота @PostBot в формате: \n<pre>[@PostBot 65fa57561ccfa]</pre> \n<i><u>вместе с квадратными скобками</u></i>',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👈 Назад', callback_data='button_spam_settings')],
        ])
        )
    

# Удалить все сслыки
@dp.callback_query(F.data == 'dell_lincks')
async def dell_lincks(query: CallbackQuery, state: FSMContext):
    links_manager.delete_all_links()
    await button_spam_settings(query, state)


# Сохранение ссылки в базу
@dp.message(MyForm.link)
async def link_save(message: Message, state: FSMContext):
    await message.delete()
    
    if message.text[:5] == 'https':
        messgae_split_space = message.text.split(' ')
        if len(messgae_split_space) == 1:
            message_split = message.text.split('/')
            msg_id = message_split[4]
            link = f'{message_split[0]}//{message_split[2]}/{message_split[3]}/'
            links_manager.insert_link(link=link, msg_id=int(msg_id), count_msg=200)

        if len(messgae_split_space) == 2:
            message_split = messgae_split_space[0].split('/')
            msg_id = message_split[4]
            link = f'{message_split[0]}//{message_split[2]}/{message_split[3]}/'
            links_manager.insert_link(link=link, msg_id=int(msg_id), count_msg=int(messgae_split_space[1]))

    if message.text[:6] == '[@Post':
        messgae_split_space = message.text.split(' ')
        if len(messgae_split_space) == 2:
            links_manager.insert_link(link=messgae_split_space[0][1:], msg_id=messgae_split_space[1][:-1], count_msg=200)

        if len(messgae_split_space) == 3:
            links_manager.insert_link(link=messgae_split_space[0][1:], msg_id=messgae_split_space[1][:-1], count_msg=int(messgae_split_space[2]))


    await message.answer(
        text='Ссылка сохранена, можно отправить ещё',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='👈 Назад', callback_data='button_spam_settings')],
        ])
        )

