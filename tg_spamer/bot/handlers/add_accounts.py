import os
import shutil
from zipfile import ZipFile

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, bot
from tg_spamer.clients import update_clients_list



class MyForm(StatesGroup):
    add_accounts = State()


# Настройки аккаунтов
@dp.callback_query(F.data == 'add_accounts_settings')
async def add_accounts_settings(query: CallbackQuery, state: FSMContext):
    await state.set_state(MyForm.add_accounts)
    builder = InlineKeyboardBuilder()

    builder.button(text='👈 Назад', callback_data='back')

    builder.adjust(1) # Кнопки вертикально
    await query.message.edit_text(
            text='Отправьте аккаунты в формате tdata запакованные в zip архив',
            reply_markup=builder.as_markup()
            )
    

@dp.message(MyForm.add_accounts, F.document)
async def await_add_accounts(message: Message, state: FSMContext):
    await message.delete()
    downloaded_file = await bot.download(file=message.document)

    with ZipFile(file=downloaded_file, metadata_encoding='cp866') as file_zip:
        files_names = file_zip.namelist()
        files = []
        for file_name in files_names:
            if file_name.find('key_datas') != -1 or file_name.find('D877F783D5D3EF8Cs') != -1 or file_name.find('maps') != -1:
                files.append(file_name)
        
        file_zip.extractall('tg_spamer/accounts', members=files)

    await update_clients_list()

    