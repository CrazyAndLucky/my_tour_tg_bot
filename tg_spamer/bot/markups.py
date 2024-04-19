from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



menu_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔘 РАССЫЛКА', callback_data='button_spam_settings')],
            [InlineKeyboardButton(text='🔍 ОБНОВИТЬ СПИСОК АККАУНТОВ', callback_data='check_accounts')],
            [InlineKeyboardButton(text='💾 ДОБАВИТЬ АККАУНТЫ', callback_data='add_accounts_settings')],
            [InlineKeyboardButton(text='🖥 ПОМЕНЯТЬ СТАТУС АККАУНТОВ', callback_data='status_accounts_settings')],
            [InlineKeyboardButton(text='⚙️ НАСТРОЙКИ', callback_data='spam_settings')],
        ])


message_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='💬 Прочитать', callback_data='send_read_messages'),
             InlineKeyboardButton(text='🗑 Удалить', callback_data='delete_dialog')],
        ])