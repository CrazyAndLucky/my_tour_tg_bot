import asyncio
import logging
from multiprocessing import Process

from aiogram import filters, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from loader import dp, bot, db, um, users, admins
from shop_bot.app import dp, cmd_start
from tg_spamer.main import tg_spamer_start
from tg_spamer.bot.bot import dp, bot
from msg_text import tg_spamer_info


# Старт
@dp.message(filters.CommandStart())
async def process_start_bot(message: Message, state: FSMContext):
    # Сохраняем пользователя в базе
    await um.add_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Перезапустить бота'),
            BotCommand(command='tg_spamer', description='Бот-интерфейс для тг спамера'),
            BotCommand(command='shop', description='Бот-магазин'),
            ]
    )

    await state.clear()
    
    await message.answer(
        text=f'Привет, {message.from_user.first_name}!',
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        text='Это своего рода бот-визитка, здесь можно посмотерть примеры моих работ!\n\nВыбирай, с помощью кнопок ниже, пример какого бота запустить',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🛍 БОТ-МАГАЗИН', callback_data='shop_bot')],
            [InlineKeyboardButton(text='💻 БОТ-ИНТЕРФЕЙС ДЛЯ ТГ СПАМЕРА', callback_data='tg_spamer_info')],
            ]),
        )


@dp.callback_query(F.data == 'tg_spamer_info')
async def tg_spamer(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text=tg_spamer_info,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='➡️ ПРОДОЛЖИТЬ', callback_data='tg_spamer')],
            ]
        ),
    )


@dp.message(filters.Command('tg_spamer'))
async def tg_spamer(message: Message, state: FSMContext):
    await message.answer(
        text=tg_spamer_info,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='➡️ ПРОДОЛЖИТЬ', callback_data='tg_spamer')],
            ]
        ),
    )


@dp.callback_query(F.data == 'shop_bot')
async def shop_bot(query: CallbackQuery, state: FSMContext):
    await cmd_start(query, state)


async def main():
    await db.connect()
    await db.create_tables()
    logging.basicConfig(level='INFO')
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    # prc = Process(target=tg_spamer_start, daemon=True, name='tg_spammer')
    # prc.start()

    asyncio.run(main())