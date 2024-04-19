import os
import shutil
from datetime import datetime, timedelta

from opentele.tl import TelegramClient
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
from opentele.exception import OpenTeleException

from tg_spamer.config import start_count_messages
from tg_spamer.loader import db, Proxy, Accounts



proxy_manager = Proxy()
acc = Accounts()


# Создать список сессий
async def get_clients(distribute_proxies: bool = False) -> dict:
    path_to_tdata: dict = get_path_to_tdata()

    clients_list = {} # Словарь запущенных сессий

    for unique_id, path in path_to_tdata.items():
        # api = API.TelegramAndroid.Generate(unique_id=unique_id)
        api = API.TelegramDesktop.Generate(unique_id=unique_id)

        try:
            tdesk = TDesktop(path)


            # Определяем прокси для аккаунта
            # Проверяем есть ли уже такой аккунт
            account = acc.get_acc_info_by_unique_id(unique_id)
            if account:
                if distribute_proxies and account[3] == 'нет прокси': # Нужно ли распределить прокси
                    proxy = proxy_manager.get_one_proxy()
    
                    if proxy is None:
                        proxy = 'miss'
                    else:
                        # Обновляем данные об аккаунте
                        acc.post_acc(unique_id=unique_id, proxy=proxy, status='новый')
                # Если не нужно распределить, то достаем прокси из базы
                else:
                    proxy = account[2]

            
            else:
                status = 'новый'
                if distribute_proxies: # Нужно ли распределить прокси
                    proxy = proxy_manager.get_one_proxy()
                    # Если нет сохраненных прокси
                    if proxy is None:
                        proxy = 'miss'
                        status = 'нет прокси'
                        # Добавляем новый аккаунт
                    
                    acc.post_acc(unique_id=unique_id, path_to_tdata=path, proxy=proxy, status=status, time=datetime.now(), proxy_type='обычный', messages=start_count_messages, spam_messages=5)
                # Если не нужно то вставляем в базу без прокси
                else:
                    proxy = 'miss'
                    status = 'нет прокси'
                    acc.post_acc(unique_id=unique_id, path_to_tdata=path, proxy=proxy, status=status, time=datetime.now(), proxy_type='обычный', messages=start_count_messages, spam_messages=5)


            # Если есть прокси создаем подключение к аккаунту
            if proxy != 'miss':
                if proxy != 'No':
                    proxy = proxy_manager.pars_proxy(proxy)
                else:
                    proxy = None

                if proxy is not False:
                    client: TelegramClient = await TelegramClient.FromTDesktop(
                        account=tdesk, 
                        session=f'tg_spamer/sessions/{unique_id}.session', 
                        flag=UseCurrentSession, 
                        api=api,
                        proxy=proxy,
                        connection_retries=3,
                        timeout=9, 
                        raise_last_call_error=True,            
                        )
                            
                    clients_list[unique_id] = client

        except OpenTeleException:
            print(f'Не удалось загрузить аккаунт | {unique_id} | попробуйте перезайти')

    return clients_list



# Получить список путей к папкам с тдата; 
def get_path_to_tdata() -> dict:
    # Берем данные базы
    data = [a[0] for a in db.fetchall('SELECT unique_id FROM accounts')]

    # Список путей к папкам тдата
    folders_tdata = os.listdir('tg_spamer/accounts')

    # Сверяем данные с базой, если в базе нет папки то обновляем базу
    for acc in data: 
        if acc not in folders_tdata:
            db.query('DELETE FROM accounts WHERE unique_id = ?', (acc,)) # Удаляем данные из базы
            try:
                os.remove(''.join(['tg_spamer/sessions/', acc, '.session'])) # Уаляем сессию
            except FileNotFoundError:
                pass
            
    # Формируем строку с путем к папке тдата и сохраняем в словарь
    path_to_tdata = {}
    for folder_tdata in folders_tdata:
        path = os.path.join('tg_spamer/accounts', folder_tdata, 'tdata')

        if os.path.isdir(path):
            path_to_tdata[folder_tdata] = path
        else:
            print(f'Папка tdata не найдена, удаляю дирректорию | {folder_tdata} |')
            shutil.rmtree(path=os.path.join('accounts', folder_tdata))

    return path_to_tdata



# Обновление информации об аккаунтах
def update_info_accounts():
    delta = timedelta(days=1) # Таймаут
    
    # accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('прогрев',))
    accounts = acc.get_all_acc_info_by_status('прогрев')

    # Если прогрелся, меняем статус
    for account in accounts:
        time = datetime.now() - datetime.fromisoformat(account[4])
        if time > delta:
            db.query('UPDATE accounts SET status = "готов", time = ? WHERE unique_id = ?', (datetime.now(), account[0],))

    # Если отлежался меняем статус
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('отлежка',))
    for account in accounts:
        time = datetime.now() - datetime.fromisoformat(account[4])
        if time > delta:
            db.query('UPDATE accounts SET status = "готов", time = ? WHERE unique_id = ?', (datetime.now(), account[0],))



def show_info_accounts():
    info = ''
    # Сколько новых
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('новый',))
    info += f'\n{numbers_in_emoji(len(accounts))} <b>НОВЫЕ АККАУНТЫ</b>'
    for account in accounts:
        info += f'\n ┠ {account[0]} | новый аккаунт'

    # Сколько в прогреве
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('прогрев',))
    info += f'\n\n{numbers_in_emoji(len(accounts))} <b>В ПРОГРЕВЕ</b>'
    for account in accounts:
        time = datetime.now() - datetime.fromisoformat(account[4])
        info +=f'\n ┠ {account[0]} | прошло | {time.days} д. {round(time.seconds / 60 / 60, 1)} ч. | шаг | {account[8]} |'

    # Сколько готовы к рассылке
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('готов',))
    info += f'\n\n{numbers_in_emoji(len(accounts))} <b>ГОТОВЫЕ К РАССЫЛКЕ</b>'
    for account in accounts:
        info += f'\n ┠ {account[0]} | готов к рассылке'
    
    # Сколько в отлежке
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('отлежка',))
    info += f'\n\n{numbers_in_emoji(len(accounts))} <b>ПОСЛЕ РАССЫЛКИ</b>'
    for account in accounts:
        time = datetime.now() - datetime.fromisoformat(account[4])
        info += f'\n ┠ {account[0]} | после рассылки, прошло | {time.days} д. {round(time.seconds / 60 / 60, 1)} ч. |'

    # Аккаунты без прокси
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('нет прокси',))
    info += f'\n\n{numbers_in_emoji(len(accounts))} <b>БЕЗ ПРОКСИ</b>'
    for account in accounts:
        info += f'\n ┠ {account[0]} | нет прокси'

    # Аккаунты в спам блоке
    accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('спам',))
    info += f'\n\n{numbers_in_emoji(len(accounts))} <b>В СПАМ БЛОКЕ</b>'
    for account in accounts:
        time = datetime.now() - datetime.fromisoformat(account[4])
        info += f'\n ┠ {account[0]} | в спам блоке, прошло | {time.days} д. {round(time.seconds / 60 / 60, 1)} ч. |'


    return info


def numbers_in_emoji(numbers: int):
    emoji = ('0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣')

    msg = ''
    for number in str(numbers):
        if number == '0': msg += emoji[0]
        if number == '1': msg += emoji[1]
        if number == '2': msg += emoji[2]
        if number == '3': msg += emoji[3]
        if number == '4': msg += emoji[4]
        if number == '5': msg += emoji[5]
        if number == '6': msg += emoji[6]
        if number == '7': msg += emoji[7]
        if number == '8': msg += emoji[8]
        if number == '9': msg += emoji[9]

    return msg


def transliteration_str(text: str) -> str:
    transliteration_data = {
    'А': 'A', '	Б': 'B', 'В': 'V',
    'Г': 'G', 'Д': 'D', 'Е': 'E',
    'Ё': 'JO', 'Ж': 'ZH', 'З': 'Z',
    'И': 'I', 'Й': 'JJ', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'KH', 'Ц': 'C',
    'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHH',
    'Ы': 'Y', 'Э': 'EH', 'Ю': 'JU',
    'Я': 'JA'
    }

    text = text.strip().upper()
    translit_text = ''
    for symbol in text:
        if symbol in transliteration_data.keys():
            translit_text += transliteration_data[symbol]
    
    return translit_text.lower()