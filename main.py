import asyncio
import logging

from aiogram import filters, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from loader import dp, bot, db, um, users, admins


# Старт
@dp.message(filters.CommandStart())
async def process_start_bot(message: Message, state: FSMContext):    
    # Сохраняем пользователя в базе
    await um.add_new_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Перезапустить бота'),
            ]
    )

    await state.clear()
    
    await message.answer(
        text=f'Привет, {message.from_user.first_name}!',
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        text='Это своего рода бот-визитка, здесь можно посмотерть примеры моих работ!\n\nВыбирай пример какого бота запустить с помощью кнопок ниже',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='БОТ-МАГАЗИН', callback_data='shop_bot')]
            ]),
        )

    


@dp.callback_query(F.data == 'shop_bot')
async def shop_bot(query: CallbackQuery, state: FSMContext):
    from shop_bot.app import dp, cmd_start

    await cmd_start(query, state)


async def main():
    await db.connect()
    await db.create_tables()
    logging.basicConfig(level='INFO')
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())
