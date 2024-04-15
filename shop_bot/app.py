import asyncio
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import filters, F
from logging import basicConfig, INFO
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_default import BotCommandScopeDefault
from aiogram.fsm.context import FSMContext

import shop_bot.handlers
from shop_bot.keyboards import menu_admin_markup, menu_user_markup, menu_main_admin_markup
from loader import bot, dp, db, admins, users


start_message = '''
Привет! Это тестовый магазин, здесь можно посмотреть примерный функционал, купить или создать новый товар.

Если хочешь поменять режим, напирмер стать админом или юзером, либо перезапусти бота либо введи команду /shop
'''

# Запуск бота
@dp.message(filters.Command('shop'))
async def cmd_start_msg(message: Message, state: FSMContext):     
     await bot.set_my_commands(
          commands=[
               BotCommand(command='start', description='Перезапустить бота'),
               BotCommand(command='shop', description='Открыть магазин')
          ]
     )
     
     for index, value in enumerate(admins):
          if message.from_user.id == value:
               try:
                    del admins[index]
               except IndexError:
                    pass
               try:
                    del users[index]
               except IndexError:
                    pass
               
     await state.clear() # Очищаем статус, если он был
     
     text = f'Выберите как открыть магазин, в режиме админа или пользователя\n\n(если потом захотите поменять, просто перезапустите бота)'
     await message.answer(
          text=text,
          reply_markup=InlineKeyboardMarkup(inline_keyboard=[
               [InlineKeyboardButton(text='Юзер', callback_data='user_mode')],
               [InlineKeyboardButton(text='Админ', callback_data='admin_mode')]
               ],
               resize_keyboard=True
               ),
     )


@dp.callback_query(F.data == 'shop_bot')
async def cmd_start(query: CallbackQuery, state: FSMContext):
     await bot.set_my_commands(
          commands=[
               BotCommand(command='start', description='Перезапустить бота'),
               BotCommand(command='shop', description='Открыть магазин')
               ]
     )
     
     for index, value in enumerate(admins):
          if query.message.from_user.id == value:
               try:
                    del admins[index]
               except IndexError:
                    pass
               try:
                    del users[index]
               except IndexError:
                    pass

     await state.clear() # Очищаем статус, если он был
     
     text = f'Выберите как открыть магазин, в режиме админа или пользователя\n\n(если потом захотите поменять, просто перезапустите бота)'
     await query.message.answer(
          text=text,
          reply_markup=InlineKeyboardMarkup(inline_keyboard=[
               [InlineKeyboardButton(text='Юзер', callback_data='user_mode')],
               [InlineKeyboardButton(text='Админ', callback_data='admin_mode')]
               ],
               resize_keyboard=True
               ),
     )



@dp.callback_query(F.data == 'admin_mode')
async def admin_mode(query: CallbackQuery, state: FSMContext):
     admins.append(query.from_user.id)
     markup = menu_main_admin_markup()
     
     await query.message.answer(
          text=start_message, 
          reply_markup=markup
          )
     

@dp.callback_query(F.data == 'user_mode')
async def user_mode(query: CallbackQuery, state: FSMContext):
     users.append(query.from_user.id)
     markup = menu_user_markup()
     
     await query.message.answer(
          text=start_message, 
          reply_markup=markup
          )

     # await state.clear() # Очищаем статус, если он был
     
     # # Проверяем нет ли его в списке пользователей
     # admins = [] 
     # data = db.fetchall('SELECT * FROM admins')

     # for value in data:
     #      admins.append(value[0])

     # if message.chat.id in admins:
     #      if message.chat.id == 1366711027:
     #           markup = menu_main_admin_markup()
     #      else:
     #           markup = menu_admin_markup()
     # else: 
     #      markup = menu_user_markup()

     #      # Сохраняем пользователя в базе, если его там нет
     #      db.query('INSERT OR REPLACE INTO users VALUES (?, 1)', (message.chat.id, ))

     # await message.answer(
     #      text=start_message, 
     #      reply_markup=markup
     #      )