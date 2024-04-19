from aiogram import F
from aiogram.types import CallbackQuery

from loader import dp
from tg_spamer.message_handler import send_read_messages



@dp.callback_query(F.data == 'send_read_messages')
async def read_messages(query: CallbackQuery):
    await query.answer() # Чтобы кнопка не моргала :)

    message_from_bot = query.message.text

    # Уникальны ид спам-аккаунта        
    msg_split = message_from_bot.split('*')
    unique_id_raw = msg_split[0]
    unique_id = unique_id_raw[1:]

    # Ид спам-юзера 
    user_id_raw = msg_split[1]
    user_id = int(user_id_raw[4:])

    # Читаем диалог
    await send_read_messages(unique_id, user_id)
    await query.message.unpin()
