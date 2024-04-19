import asyncio
import logging

from aiogram import F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, BotCommand, BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

from tg_spamer.loader import db
from tg_spamer.message_handler import send_msg_to_user, get_media_from_msg
from tg_spamer.bot.handlers import dp, event_forward_m_stop, event_forward_m_start
from tg_spamer.functions import acc_info
from tg_spamer.bot.markups import message_markup, menu_markup
from tg_spamer.tools import show_info_accounts
from tg_spamer.clients import update_clients_list
from tg_spamer.config import chat_id
from loader import dp, bot



event_update = asyncio.Event()


async def send_chat_audio(file):
    await bot.send_audio(chat_id=chat_id, audio=BufferedInputFile(file=file, filename='audio'))


async def send_chat_photo(file):
    await bot.send_photo(chat_id=chat_id, photo=BufferedInputFile(file=file, filename='photo'))


async def send_chat_video(file):
    await bot.send_video(chat_id=chat_id, video=BufferedInputFile(file=file, filename='vodeo'))


# Отправляем историю диалога в чат 
async def send_history_dialog(text):
    usr_id = text.split('*')[1]
    # Если сообщеине есть то редактируем или отправляем новое
    message_data = db.fetchone('SELECT * FROM mes_in_chat WHERE usr_id = ?', (usr_id,))
    try:
        if message_data:
            try:
                await bot.edit_message_text(chat_id=chat_id, text=text, message_id=message_data[1], link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=message_markup)
                # await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_data[1], reply_markup=message_markup)
                
                await bot.unpin_chat_message(chat_id=chat_id, message_id=message_data[1])
                await bot.pin_chat_message(chat_id=chat_id, message_id=message_data[1])
                print('Отредактирвоал сообщение', usr_id)
            
            except TelegramBadRequest as e:
                if 'message is not modified' in str(e):
                    print('В диалоге нет новых сообщений')
            
                else:
                    mes = await bot.send_message(chat_id=chat_id, text=text, link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=message_markup)
                    await bot.pin_chat_message(chat_id=chat_id, message_id=mes.message_id)
                    db.query('INSERT OR REPLACE INTO mes_in_chat VALUES (?, ?)', (usr_id, mes.message_id))
                    print('Отправил новое сообщение', usr_id)
        
        else:
            mes = await bot.send_message(chat_id=chat_id, text=text, link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=message_markup)
            await bot.pin_chat_message(chat_id=chat_id, message_id=mes.message_id)
            db.query('INSERT OR REPLACE INTO mes_in_chat VALUES (?, ?)', (usr_id, mes.message_id))
            print('Отправил новое сообщение', usr_id)
    
    except TelegramRetryAfter as e:
        print('Ошбика попробую через', e.retry_after)
        await asyncio.sleep(e.retry_after)
        await send_history_dialog(text)
    

# Возврат в меню
@dp.callback_query(F.data == 'back')
async def back(query: CallbackQuery, state: FSMContext):
    # Очищаем состояния, если они есть
    await state.clear()
    try:
        await query.message.delete()
    except Exception:
        pass

    info = show_info_accounts()
    await query.message.answer(
        text=info,
        reply_markup=menu_markup
        )

# Проверить аккаунты 
@dp.callback_query(F.data == 'check_accounts')
async def check_accounts(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text='⌛')
    await update_clients_list()
    await acc_info(connect=True)
    await back(query, state)


# Открыть меню
# @dp.message(Command('menu'))
@dp.callback_query(F.data == 'tg_spamer')
async def handler_message(query: CallbackQuery, state: FSMContext):
    # Очищаем состояния, если они есть
    await state.clear()
    try:
        await query.message.delete()
    except Exception:
        pass

    info = show_info_accounts()
    await query.message.answer(
        text=info,
        reply_markup=menu_markup
        )


# Обновить диалоги
@dp.message(Command('update'))
async def update_chat_data(message: Message):
    await message.delete()
    event_update.set()


# Обновляем истоирю диалога в чате
@dp.message(Command('это чтобы не запустить:)'))
async def handler_message(message: Message):
    # Если сообщение в чате для рассылки
    if message.chat.id == int(chat_id):
        # Если ответили на сообщение бота
        if message.reply_to_message:
            if message.pinned_message:
                await message.delete()

            else:
                message_from_bot = message.reply_to_message.text
                
                # Получаем ид аккаунта которому нужно отправить сообщение
                msg_split = message_from_bot.split('*')
                unique_id_raw = msg_split[0]
                unique_id = unique_id_raw[1:]

                # Получаем ид пользователя 
                user_id_raw = msg_split[1]
                user_id = int(user_id_raw[4:])

                await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

                if 'voice:' in message.text:
                    file = await get_media_from_msg(unique_id, user_id, int(message.text[6:]))
                    await send_chat_audio(file)

                elif 'video:' in message.text:
                    file = await get_media_from_msg(unique_id, user_id, int(message.text[6:]))
                    await send_chat_video(file)

                elif 'photo:' in message.text:
                    file = await get_media_from_msg(unique_id, user_id, int(message.text[6:]))
                    await send_chat_photo(file)

                elif 'sticker:' in message.text:
                    file = await get_media_from_msg(unique_id, user_id, int(message.text[8:]))
                    await send_chat_photo(file)


                else: 
                    # Редактируем сообщение в чате
                    message_from_bot_raw = message_from_bot.split('\n')
                    f_line = f'{message_from_bot_raw.pop(0)}'
                    
                    while True:
                        f_line_raw = f_line
                        for part_message in message_from_bot_raw:
                            f_line_raw += f'\n{part_message}'
                        
                        # f_line_raw += f'\n➖➖{str(message.date.strftime("%m-%d, %H:%M"))}➖➖\n'
                        f_line_raw += '\n➖➖➖➖➖➖➖➖➖➖➖➖\n'
                        f_line_raw += f'⬆️ {message.text}'

                        if len(f_line_raw) > 3900:
                            message_from_bot_raw.pop(0)
                            continue
                        else:
                            f_line = f_line_raw 
                            break
                    
                    await message.reply_to_message.edit_text(f_line, link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=message_markup)
                    # await message.reply_to_message.edit_reply_markup(reply_markup=message_markup)

                    await bot.unpin_chat_message(chat_id=chat_id, message_id=message.reply_to_message.message_id)

                    # Отправляем сообщение пользователю
                    await send_msg_to_user(unique_id, message.text, user_id)


async def bot_main() -> None:
    pass
    # logging.basicConfig(level=logging.INFO)

    # await bot.set_my_commands(commands=[
    #     BotCommand(command='update', description='Обновить диалоги'),
    #     BotCommand(command='menu', description='Открыть меню')
    #     ])

    