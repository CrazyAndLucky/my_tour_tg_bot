import asyncio

from opentele.tl import TelegramClient

from tg_spamer.loader import db
from tg_spamer.clients import clients_list, config
from tg_spamer.handlers import spammer
from tg_spamer.tools import show_info_accounts
from tg_spamer.account_in_out import connect_account



# Проверяем и обновляем данные об аккаунтах
async def acc_info(connect: bool = None):
    accounts = [] 
    if connect:
        for unique_id, client in clients_list.items():
            accounts.append(connect_account(client, unique_id, client_disconnect=True))

        await asyncio.gather(*accounts)
    
    # Инфа об аккаунтах
    # update_info_accounts()
    print(show_info_accounts())


async def mass_connect(accounts: dict):
    tasks_connect = []
    for unique_id, client in accounts.items():
        tasks_connect.append(connect_account(client, unique_id))

    await asyncio.gather(*tasks_connect)


async def mass_disconnect():
    tasks_disconnect = []
    for unique_id, client in clients_list.items():
        print(f'| {unique_id} | дисконнект')
        client: TelegramClient
        # if client.is_connected():
        tasks_disconnect.append(client.disconnect())
    
    await asyncio.gather(*tasks_disconnect)
    print('Завершил дисконнект')



# Рассылка войса
async def spam_voice(dual_send: bool):
    accounts = {account[0]:clients_list[account[0]] for account in db.fetchall('SELECT * FROM accounts WHERE status = "готов"')}

    # Очищаем логи
    config.clear_log_file()

    # Коннект
    await mass_connect(accounts)
    
    # Рассылка
    tasks_spam = []
    for unique_id, client in accounts.items():
        if dual_send:
            tasks_spam.append(spammer(client, unique_id, voice=True, dual_send=True))
        else:
            tasks_spam.append(spammer(client, unique_id, voice=True))

    await asyncio.gather(*tasks_spam)

    # После рассылки дисконнект
    await mass_disconnect()

    # Сохраняем в логи общее кол-во отправленные сообщений
    config.save_logs_count_msg()



async def spam_message_button(user_b: list, dual_send: bool = None, postbot: bool = None):
    accounts = {account[0]:clients_list[account[0]] for account in db.fetchall('SELECT * FROM accounts WHERE status = "готов"')}

    # Очищаем логи
    config.clear_log_file()

    # Коннект
    await mass_connect(accounts)

    # Рассылка
    tasks_spam = []
    for unique_id, client in accounts.items():
        if postbot:
            if dual_send:
                tasks_spam.append(spammer(user_b, client, unique_id, postbot=True, dual_send=True))
            else:
                tasks_spam.append(spammer(user_b, client, unique_id, postbot=True))
        else: 
            if dual_send:
                tasks_spam.append(spammer(user_b, client, unique_id, link=True, dual_send=True))
            else:
                tasks_spam.append(spammer(user_b, client, unique_id, link=True))

    await asyncio.gather(*tasks_spam)

    # После рассылки дисконнект
    await mass_disconnect()

    # Сохраняем в логи общее кол-во отправленные сообщений
    config.save_logs_count_msg()