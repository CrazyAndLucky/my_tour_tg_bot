from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from tg_spamer.loader import db
from loader import dp, bot
from tg_spamer.clients import config



class MyCallback(CallbackData, prefix='spam'):
    step: str
    action: str


class MyForm(StatesGroup):
    await_users = State()
    await_delay = State()



@dp.callback_query(F.data == 'spam_settings')
async def spam_settings(query: CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()

    if config.dual_message() == 0: 
        builder.button(text='❌ Двойная отправка', callback_data=MyCallback(step='settings_dual_send', action='no'))   
    else:
        builder.button(text='✅ Двойная отправка', callback_data=MyCallback(step='settings_dual_send', action='yes'))

    builder.button(text='⏰ Поменять задержку', callback_data='change_delay')
    builder.button(text='✉️ Поменять кол-во сообщений', callback_data='change_count_message')
    builder.button(text='👥 Аудитория для рассылки', callback_data='users_send')
    builder.button(text='🔗 Проски', callback_data='info_proxy')
    builder.button(text='👈 Назад', callback_data='back')

    builder.adjust(1) # Кнопки вертикально
    delay = config.raw_delay().split(' ')
    text = f'<b>НАСТРОЙКИ РАССЫЛКИ</b>\n\nЗадержка между сообщенями от <b>{delay[0]}</b> до <b>{delay[1]}</b> секунд'
    
    await query.message.delete()
    await query.message.answer(
            text=text,
            reply_markup=builder.as_markup()
            )

    
            

# Замена задержки сежду сообщениями
@dp.callback_query(F.data == 'change_delay')
async def change_delay(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text='Отправьте два числа пробел 10 30')
    await state.set_state(MyForm.await_delay)


# Ожидаю сообщения с цифрами задержки
@dp.message(MyForm.await_delay)
async def save_change_delay(message: Message, state: FSMContext):
    if config.change_delay(message.text):
        await message.answer(
            text='Задержка сохранена',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Продолжить', callback_data='spam_settings')]
            ])
            )
    else:
        await message.answer(text='Неверный формат задержки, поробуйте ещё раз')


# Двойная отправка
@dp.callback_query(MyCallback.filter(F.step == 'settings_dual_send'))
async def settings_dual_send(query: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    action = callback_data.action
    if action == 'yes':
        db.query('UPDATE config SET dual_message = 0')
        await spam_settings(query, state)
    
    if action == 'no':
        db.query('UPDATE config SET dual_message = 1')
        await spam_settings(query, state)


# Пользователи для спама
@dp.callback_query(F.data == 'users_send')
async def users_send(query: CallbackQuery):
    await query.message.edit_text(text='Аудитория для рассылки 👇')
    await query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Заменить', callback_data='change_users_send')],
            [InlineKeyboardButton(text='👈 Назад', callback_data='spam_settings')]
        ])
        )

    # Достаем спам-юзеров из базы, формируем строку, преобразуем в байты и отправляем как txt
    row_users = config.get_spam_users()
    if row_users:
        users_str = ''
        for user in row_users:
            users_str += f'{user}\n'

        users_bytes = users_str.encode()
        await query.message.answer_document(document=BufferedInputFile(file=users_bytes, filename='users.txt'))
    else:
        await query.answer(text='Пользователей для рассылки нет', show_alert=True)


# Заменить аудиторию для рассылки
@dp.callback_query(F.data == 'change_users_send')
async def users_send(query: CallbackQuery, state: FSMContext):
    await state.set_state(MyForm.await_users)
    await query.message.answer(
        text='Отправьте список пользователей',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='👈 Назад', callback_data='back_users_send')]
            ])
        )


# Отмена загрузки списка пользователей
@dp.callback_query(F.data == 'back_users_send')
async def back_users_send(query: CallbackQuery, state: FSMContext):
    await spam_settings(query, state)
    

# Сохранение спам-юзеров в базе 
@dp.message(MyForm.await_users, F.document)
async def await_users_send(message: Message, state: FSMContext):
    # Достаем пользователей из текста
    row_users = (await bot.download(file=message.document)).read().decode()
    users = row_users.strip().split('\n')

    # Очищаем базу и сохраняем пользователей
    config.delete_all_spam_users()
    for user in users:
        user = user.strip()
        config.insert_spam_user(user)

    # Возвращаемся в меню
    await state.clear()
    await message.answer(
        text='Сохранил пользователей',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Продолжить', callback_data='spam_settings')]
        ])
        )