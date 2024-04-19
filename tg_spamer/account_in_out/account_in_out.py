import os
import shutil

from opentele.tl import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError

from tg_spamer.loader import db
from tg_spamer.clients import clients_list, accounts_manager



# Удаление аккаунта 
async def delete_account(client: TelegramClient, unique_id):
    try:
        # Выход работает даже на забаненных аккаунтах, при выходе удаляется файл сессии
        await client.log_out()

        # os.remove(''.join(['sessions/', unique_id, '.session'])) 
        shutil.rmtree(''.join(['accounts/', unique_id]))
    except Exception as e:
        print(f'| {unique_id} | Не получилось удалить файл сессии {e}')

    # Также удаляю запись из базы
    db.query('DELETE FROM accounts WHERE unique_id = ?', (unique_id,))


# Проверяет аккаунт на бан, если забанен удаляет
async def connect_account(client: TelegramClient, unique_id, client_disconnect: bool = None):
    client: TelegramClient
    try:
        status = db.fetchone('SELECT status FROM accounts WHERE unique_id = ?', (unique_id,))[0]

        if status != 'нет прокси':
            await client.connect()
            print(f'| {unique_id} | коннект')

        # Проверка аккаунта на бан
        me = await client.get_me()
        if me is None:
            print(f'Аккаунт забанен, удаляю | {unique_id} |')
            # Отключаюсь и удаляю файл сессии 
            # await client.disconnect()
            await delete_account(client, unique_id)
            del clients_list[unique_id]
        else:
            # Сохраняем номер телефона в базе
            accounts_manager.post_acc(unique_id=unique_id, phone=me.phone)
            
        
        if client_disconnect:
            await client.disconnect()
        
    except TypeError:
        print(f'| {unique_id} | проблема с прокси')
        await client.disconnect()
        await edit_proxy(client, unique_id)

    except ConnectionError:
        print(f'| {unique_id} | проблема с прокси')
        await client.disconnect()
        await edit_proxy(client, unique_id)
    
    except AuthKeyDuplicatedError:
        print(f'| {unique_id} | ошибка авторизации, аккаут выбило, удаляю')
        # await client.disconnect()
        await delete_account(client, unique_id)
        del clients_list[unique_id]
        


# Замена прокси
async def edit_proxy(client: TelegramClient, unique_id):
    db.query('UPDATE accounts SET status = ? WHERE unique_id = ?', ('нет прокси', unique_id))
    
    del clients_list[unique_id]