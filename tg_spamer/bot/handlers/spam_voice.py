from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from loader import dp, bot
from tg_spamer.functions import spam_voice
from tg_spamer.clients import config, accounts_manager



class MyCallback(CallbackData, prefix='spam'):
    step: str
    action: str


class MyForm(StatesGroup):
    voice_note = State()


# Аудио для рассылки
@dp.callback_query(F.data == 'spam_voice')
async def prep_voice(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer_audio(audio=FSInputFile(path='tg_spamer/data/voice.mp3', filename='voice'))
    await query.message.answer(
        text='Аудио для рассылки ☝️',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔄 Заменить', callback_data=MyCallback(step='prep_voice', action='yes').pack())],
            [InlineKeyboardButton(text='✅ Продолжить', callback_data=MyCallback(step='prep_voice', action='no').pack())],
            [InlineKeyboardButton(text='👈 Назад', callback_data='back')],
            ]),
        )


# Выбор: запись войса или продолжение
@dp.callback_query(MyCallback.filter(F.step == 'prep_voice'))
async def await_voice(query: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    action = callback_data.action
    if action == 'no':
        await confirm_voice(query=query)    
    else:
        await state.set_state(MyForm.voice_note)
        await query.message.delete()
        await query.message.answer(text='Запишите новый войс:', 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='👈 Назад', callback_data='stop_await_voice')],
            ])
        )


# Отмена записи войса
@dp.callback_query(F.data == 'stop_await_voice')
async def note_voice(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await prep_voice(query)


# Ожидание войса и загрузка его
@dp.message(MyForm.voice_note, F.voice)
async def note_voice(message: Message, state: FSMContext):
    await state.clear()
    await bot.download(file=message.voice, destination='tg_spamer/data/voice.mp3')
    print('Сохранил войс')

    await confirm_voice(message=message)
    

# Подтверждение рассылки
async def confirm_voice(query: CallbackQuery = None, message: Message = None):
    accounts = accounts_manager.get_all_acc_info_by_status('готов')
    if accounts:
        text = '<b>⬇️РАССЫЛКА ГОЛОСОВОГО СООБЩЕНИЯ⬇️</b>\n'
        for account in accounts:
            text += f'| {account[0]} | доступно сообщений | {account[6]} |\n'


        dual_message = config.dual_message()
        if dual_message == 1:
            text += '\nДвойная отправка: ✅'
        else:
            text += '\nДвойная отправка: ❌'


    if query:
        await query.message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Подтвердить', callback_data=MyCallback(step='confirm_voice', action='yes').pack())],
            [InlineKeyboardButton(text='❌ Отмена', callback_data=MyCallback(step='stop_confirm_voice', action='yes').pack())],
        ])
        )
    
    if message:
        await message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Подтвердить', callback_data=MyCallback(step='confirm_voice', action='yes').pack())],
            [InlineKeyboardButton(text='❌ Отмена', callback_data=MyCallback(step='stop_confirm_voice', action='yes').pack())],
        ])
        )


# Отмена рассылки
@dp.callback_query(MyCallback.filter(F.step == 'stop_confirm_voice'))
async def send_voice(query: CallbackQuery, callback_data: MyCallback):
    await prep_voice(query)


# Начинаю рассылку войса
@dp.callback_query(MyCallback.filter(F.step == 'confirm_voice'))
async def send_voice(query: CallbackQuery, callback_data: MyCallback):
    print('Начинаю')
    await query.message.delete()
    await query.message.answer(text='Начинаю рассылку')
    
    # Сохраняю те аккаунты, которые будут в рассылке
    spam_accounts = accounts_manager.get_unique_id_by_status(status='готов')
    
    # Двойная отправка
    dual_send = config.dual_message()
    await spam_voice(dual_send)

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
