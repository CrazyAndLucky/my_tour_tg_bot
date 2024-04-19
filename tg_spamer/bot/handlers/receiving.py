import asyncio

from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.exceptions import TelegramBadRequest

from tg_spamer.loader import db
from loader import dp, bot
from tg_spamer.clients import config, clients_list



event_forward_m_start = asyncio.Event()
event_forward_m_stop = asyncio.Event()


# Прием сообщений
@dp.callback_query(F.data == 'receiving_messages')
async def settings_receiving_message(query: CallbackQuery):
    await query.message.delete()
    
    # Определяем вкдючен ли прием сообщеинй
    if event_forward_m_start.is_set():
        text = 'Прием сообщений'
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='✅', callback_data='turn_of_receiving')],
                [InlineKeyboardButton(text='👈 Назад', callback_data='back')],
                ]
            )
    else:
        text = 'Прием сообщений'
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❌', callback_data='turn_on_receiving')],
                [InlineKeyboardButton(text='👈 Назад', callback_data='back')],
                ]
            )
    
    
    await query.message.answer(
        text=text,
        reply_markup=markup,
    )


@dp.callback_query(F.data == 'turn_on_receiving')
async def turn_on_receiving(query: CallbackQuery):
    for unique_id, client in clients_list.items():
            account = db.fetchone('SELECT * FROM accounts WHERE unique_id = ?', (unique_id,))
            if account[3] == 'готов' or account[3] == 'отлежка':
                event_forward_m_start.set()
    
    await settings_receiving_message(query)


@dp.callback_query(F.data == 'turn_of_receiving')
async def turn_of_receiving(query: CallbackQuery):
    event_forward_m_stop.set()
    await settings_receiving_message(query)