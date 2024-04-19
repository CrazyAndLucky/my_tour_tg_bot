import os
from random import randint
from datetime import datetime, timedelta
import logging
import re

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from opentele.tl import TelegramClient
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
from opentele.exception import OpenTeleException

from tg_spamer.data import DB_Manager
from tg_spamer.config import get_users



db = DB_Manager('tg_spamer/data/data.db')
db.create_tables()

logger = logging.getLogger(name='Spam_Info')


class Accounts():
    def __init__(self) -> None:
        pass

    def get_unique_id_by_status(self, status: str) -> list:
        accounts = [unique_id[0] for unique_id in db.fetchall('SELECT * FROM accounts WHERE status = ?', (status,))]

        return accounts


    def get_all_acc_info_by_status(self, status: str):
        account = db.fetchall('SELECT * FROM accounts WHERE status = ?', (status,))

        return account


    def get_acc_info_by_unique_id(self, unique_id: str):
        account = db.fetchone('SELECT * FROM accounts WHERE unique_id = ?', (unique_id,))

        return account
    
    
    def post_acc(self, unique_id=str, path_to_tdata=None, proxy=None, status=None, time=None, proxy_type=None, messages=None, spam_messages=None, step=None, phone=None):
        account = self.get_acc_info_by_unique_id(unique_id)

        if account:
            if path_to_tdata is None:
                path_to_tdata = account[1]

            if proxy is None:
                proxy = account[2]

            if status is None:
                status = account[3]

            if time is None:
                time = account[4]

            if proxy_type is None:
                proxy_type = account[5]

            if messages is None:
                messages = account[6]

            if spam_messages is None:
                spam_messages = account[7]

            if step is None:
                step = account[8]

            if phone is None:
                phone = account[9]
                
                
            db.query(
                'UPDATE accounts SET path_to_tdata = ?, proxy = ?, status = ?, time = ?, proxy_type = ?, messages = ?, spam_messages = ?, step = ?, phone = ? WHERE unique_id = ?', 
                (path_to_tdata, proxy, status, time, proxy_type, messages, spam_messages, step, phone, unique_id)
                )
        else:
            db.query(
                'INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                (unique_id, path_to_tdata, proxy, status, datetime.now(), proxy_type, messages, 0, 1, phone)
                )


class Links():
    def __init__(self) -> None:
        pass


    # Достать из базы ссылку на пост в PostBot
    def get_one_link_postbot(self) -> None:
        links = db.fetchall('SELECT * FROM links')
        for link in links:
            if link[3] > 0 and link[1] == '@PostBot':
                return link

        print('В базе нет postbot ссылок')
        return False
    

    # Достать из базы обычную ссылку
    def get_one_link(self) -> None:
        links = db.fetchall('SELECT * FROM links')
        for link in links:
            if link[3] > 0 and link[1][:5] == 'https':
                return link

        print('В базе нет обычных ссылок')
        return False


    # Уменьшить кол-во сообщение на 1
    def decrease_count_msg(self, id):
        count_msg = self.get_count_msg(id)
        
        if count_msg == 0:
            self.delete_link(id)
            return False
        else:
            count_msg = count_msg - 1
            db.query('UPDATE links SET count_msg = ? WHERE id = ?', (count_msg, id))



    # Получить кол-во доступных сообщений для ссылки
    def get_count_msg(self, id):
        return db.fetchone('SELECT count_msg FROM links WHERE id = ?', (id,))[0]


    # Получить список всех ссылок
    def get_all_links(self) -> list:
        return db.fetchall('SELECT * FROM links')


    # Добавить ссылку в базу
    def insert_link(self, link: str, msg_id: int, count_msg: int) -> None:
        db.query('INSERT OR IGNORE INTO links (link, msg_id, count_msg) VALUES (?, ?, ?)', (link, msg_id, count_msg))


    # Удалить ссылку из базы
    def delete_link(self, id: int) -> None:
        db.query('DELETE FROM links WHERE id = ?', (id,))


    # Удалить все сслыки
    def delete_all_links(self) -> None:
        db.query('DELETE FROM links')



class Proxy():
    def __init__(self) -> None:
        pass


    # Выгрузить проски из базы
    def get_one_proxy(self) -> None:
        try:
            proxy = db.fetchone('SELECT proxy FROM proxy')[0]
            self.delete_proxy(proxy)
            return proxy
        
        except TypeError:
            print('В базе нет прокси')


    # Получить кол-во всех прокси
    def count_prixys(self) -> int:
        return db.fetchone('SELECT COUNT(*) FROM proxy')[0]
    

    # Удалить один проски из базы
    def delete_proxy(self, proxy: str) -> None:
        db.query('DELETE FROM proxy WHERE proxy = ?', (proxy,))


    # Удалить все проски из базы
    def delete_all_proxy(self) -> None:
        db.query('DELETE FROM proxy')


    # Добавить прокси в базу
    def insert_proxy(self, proxy) -> None:
        db.query('INSERT OR IGNORE INTO proxy VALUES (?)', (proxy,))

    # Получить список всех прокси
    def get_all_proxy(self) -> list:
        return [user[0] for user in db.fetchall('SELECT * FROM proxy')]
    

    # Парсинг прокси из строки
    def pars_proxy(self, proxy) -> dict:
        try:
            proxy_split = proxy.split(':')

            proxy_type = proxy_split[0]
            host = proxy_split[3]
            port = proxy_split[4]
            login = proxy_split[1]
            password = proxy_split[2]

            

            proxy = {
                'proxy_type': proxy_type, 
                'addr': host,      
                'port': int(port),           
                'username': login,      
                'password': password,                
            }

            return proxy
        
        except Exception:
            print('Не получилось спарсить прокси')
            return False


class Config:
    def __init__(self) -> None:
        pass
    
    # Сохранить в логи, кол-во отправленных сообщений
    def save_logs_count_msg(self):
        count_msg = self.get_count_send_msg()
        logger.info(f'Расссылка завершена, всего сообщений отправленно | {count_msg} |')


    # Очистить логи, также сбросить из базы кол-во отправленных сообщений
    def clear_log_file(self):
        self.clear_count_send_msg()
        with open(file='tg_spamer/logs.txt', mode='w', encoding='utf-8') as fl:
            fl.write('')


    # Информация, нужна ли двойная отправка
    def dual_message(self):
        return db.fetchone('SELECT dual_message FROM config')[0]
        

    # Сохранить пользователя в память и удалить из базы
    def get_spam_user(self) -> None:
        try:
            user = db.fetchone('SELECT username FROM spam_users')[0]
            self.delete_spam_user(user)
            return user
        
        except TypeError:
            print('В базе нет пользователей для рассылки')


    # Получить список всех пользователей
    def get_spam_users(self) -> list:
        return [user[0] for user in db.fetchall('SELECT * FROM spam_users')]


    # Добавить обратно в базу
    def insert_spam_user(self, user) -> None:
        db.query('INSERT OR IGNORE INTO spam_users VALUES (?)', (user,))


    # Удалить юзера из базы
    def delete_spam_user(self, username: str) -> None:
        db.query('DELETE FROM spam_users WHERE username = ?', (username,))


    # Очистить список спам-юзеров
    def delete_all_spam_users(self) -> None:
        db.query('DELETE FROM spam_users')


    # Получить кол-во всех юзеров 
    def count_spam_user(self) -> int:
        return db.fetchone('SELECT COUNT(*) from spam_users')[0]


    # Получить кол-во отправленных сообщений
    def get_count_send_msg(self) -> str:
        return db.fetchone('SELECT count_send_msg FROM config')[0]
    
        # with open(file='logs.txt', mode='r') as f:
        #     count = f.read()
        # return count
    
    # Увеличить кол-во отправленных сообщений
    def increase_count_send_msg(self, count_msg: int):
        msg = self.get_count_send_msg()
        db.query('UPDATE config SET count_send_msg = ?', (msg + count_msg,))


    # Очистить количество отправленных сообщений
    def clear_count_send_msg(self):
        db.query('UPDATE config SET count_send_msg = ?', (0,))
        

    # Получить кол-во доступных сообщений для отправки
    def get_msg(self, unique_id):
        return db.fetchone('SELECT messages FROM accounts WHERE unique_id = ?', (unique_id,))[0]


    # Увеличить или уменьшить кол-во доступных сообщений
    def update_msg(self, unique_id, value: int):
        msg = self.get_msg(unique_id) + value
        if msg > 20:
            msg = 20
        elif msg < 2:
            msg = 2

        db.query('UPDATE accounts SET messages = ? WHERE unique_id = ?', (msg, unique_id))

    def _update_msg(self, unique_id, value: int):
        '''Установить кол-во доступных сообщений на аккаунт на указанное число'''
        db.query('UPDATE accounts SET messages = ? WHERE unique_id = ?', (value, unique_id))


    def delay(self) -> int:
        '''Получить рандоную задержку'''
        delay_from_db = db.fetchone('SELECT spam_delay FROM config')[0].split(' ')
        delay = randint(int(delay_from_db[0]), int(delay_from_db[1]))
        return delay
    
    def raw_delay(self) -> str:
        return db.fetchone('SELECT spam_delay FROM config')[0]


    def change_delay(self, number: str) -> None:
        '''Изменить задержку между отправкой сообщений'''
        
        number_s = number.split(' ')
        if re.fullmatch(pattern='\d{1,3}\s\d{0,3}', string=number.strip()):
            if int(number_s[0]) < int(number_s[1]):
                db.query('UPDATE config SET spam_delay = ?', (number,))
                return True
            else:
                print('Неверный формат задержки 1')
                return False
        else: 
            print('Неверный формат задержки')
            return False