# from loader import db
# from datetime import datetime, timedelta
import time 
import datetime
# import os
# import shutil
# import asyncio
# from random import randint
# import multiprocessing



# with open(file='data/users.txt', mode='r', encoding='UTF-8') as file:
#     values_str = file.read()

# values = values_str.strip().split('\n')

# for value in values:
#     db.query('INSERT OR IGNORE INTO users VALUES (?)', (value,))



# db.query('INSERT INTO accounts (time) VALUES (?)', (a,))

# db.query('ALTER TABLE accounts ADD COLUMN messages INT')


# a = datetime.now()
# time.sleep(2)
# b = datetime.now()

# print((a - b).days)



# bots = list((chanel[0] for chanel in db.fetchall('SELECT * FROM bots')))

# print(bots)


# db.query('UPDATE accounts SET status = "новый" WHERE unique_id = "+27612789861"')



# a = datetime.now()

# strtime = '2024-02-09 00:57:23.629119'
# b = datetime.fromisoformat(strtime)

# c = timedelta(days=1)

# ggg = a - b

# if ggg > c:
#     print('lf')


clients_list = {
    'id1': 'client1',
    'id2': 'client2',
    'id3': 'client3',
    'id4': 'client4',
    'id5': 'client5',
    'id6': 'client6',
    'id7': 'client7',
    'id8': 'client8',
    'id9': 'client9',
    'id10': 'client10',
}


# def save_count_send_messages(send_users: int):
#     with open(file='logs.txt', mode='r', encoding='UTF-8') as fl:
#         text = fl.read()
#         if text == '':
#             text = send_users
#         else:
#             text = int(text) + send_users
            

#     with open(file='logs.txt', mode='w', encoding='UTF-8') as fl:
#         fl.write(str(text))


# def change_photo():
#     # Получаю путь к файлам фото и складыаю в список 
#     photos = os.listdir('profile_photos')
#     photos_path = []
#     for photo in photos:
#         photo_path = ''.join(['profile_photos/', photo])
#         photos_path.append(photo_path)

#     print(photos_path)


# change_photo()




# async def spam(client, id, queue: asyncio.Queue):
#     send_messages = 0
#     while True:
#         if send_messages != 2:
#             print(f'| {id} | отправленно сообщеине')
#             send_messages += 1
#             await asyncio.sleep(randint(0, 5))
#         else:
#             print(f'| {id} | работу завершил')
#             await queue.get()
#             queue.task_done
#             break



# async def main():
#     queue = asyncio.Queue(maxsize=2)

#     list_accounts = [
#         {'client-1': 'id-1', 'client-2': 'id-2'},
#         {'client-3': 'id-3', 'client-4': 'id-4'},
#         {'client-5': 'id-5', 'client-6': 'id-6'},
#     ]

#     tasks = []
#     for list_account in list_accounts:
#         for client, id in list_account.items():
#             await queue.put(id)
#             task = asyncio.create_task(spam(client, id, queue))
#             tasks.append(task)
    
#     await asyncio.gather(*tasks)
#     print(queue.full())
#     # await queue.join()

#     print('==========\nЗавершил работу')


# # asyncio.run(main())
    




# async def spam(client, id):
#     send_messages = 0
#     while True:
#         if send_messages != 2:
#             print(f'| {id} | отправленно сообщеине')
#             send_messages += 1
#             await asyncio.sleep(randint(3, 5))
#         else:
#             print(f'| {id} | работу завершил')
#             break



# async def main():
#     list_accounts = [
#         {'client-1': 'id-1', 'client-2': 'id-2'},
#         {'client-3': 'id-3', 'client-4': 'id-4'},
#         {'client-5': 'id-5', 'client-6': 'id-6'},
#     ]

#     tasks = []
#     for list_account in list_accounts:
#         for client, id in list_account.items():
#             task = asyncio.create_task(spam(client, id))
#             tasks.append(task)
            
#             if len(tasks) == 2:
#                 await asyncio.gather(*tasks)
#                 tasks.clear()
    


#     print('==========\nЗавершил работу')


# asyncio.run(main())


# async def my_task():
#     for _ in range(5):
#         print("Выполняю задачу...")
#         await asyncio.sleep(1)

# def main():
#     # Получаем текущий цикл событий
#     loop = asyncio.get_event_loop()

#     # Запускаем задачу
#     tasks = []
#     for _ in range(5):
#         task = loop.create_task(my_task())
#         tasks.append(task)
    
#     asyncio.gather(*tasks)
#     print('выполнил')
#     # Запускаем основной цикл, который будет выполняться всегда
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         print("Прервано пользователем")
#     finally:
#         # Закрываем цикл после завершения работы
#         loop.close()

# # Запускаем основную функцию
# main()


text = '''
В любом сервисе существуют определённые ограничения для пользователей — как правило, о них можно узнать из технического описания. Лимиты есть и в популярном Telegram. Вот только на официальном сайте отсутствует подробное описание всех ограничений. 

Можно поискать нужную информацию в различных публикациях или найти ограничения опытным путём. Чтобы вам не пришлось этого делать, собрала подборку основных лимитов в Telegram на момент публикации.

В конце — о платном способе расширить некоторые лимиты Telegram.

Чат-боты в Telegram —
за считаные минуты
No-code конструктор от Unisender. Простая интеграция, подробная аналитика, готовые шаблоны сценариев. 14 дней — 0 ₽.
Попробовать
чат-боты
Учётные записи
Учётная запись — это личный аккаунт пользователя, который становится доступен сразу после регистрации. И вот какие лимиты предусмотрены для пользовательского аккаунта:

Имя пользователя (username): 5–32 символов.

Длина имени: 1–64 символов.

Длина фамилии: 0–64 символов. 

Описание аккаунта (Bio): до 70 символов. 

Количество каналов и групп, в которых можно состоять: до 500.

Количество созданных публичных каналов и групп: до 10.

Длительность видеоаватара: до 10 секунд. 

Количество сохранённых GIF: до 200.

Количество папок: до 10. Как сделать папки в Telegram?

Количество чатов в папках: до 100.

Закреплённые чаты/каналы/группы/боты: до 5 + 5 секретных чатов.

Срок самоуничтожения учетной записи при неактивности в аккаунте (настраиваемая функция): через 1–12 месяцев.

Спам-бан на отправку сообщений и создание публичных каналов/групп: от 48 часов до бесконечности.

Сообщения
В Telegram разрешены достаточно объёмные сообщения. К ним можно прикреплять медиафайлы, фото и видео. Однако есть и ограничения:

Длина одного сообщения: до 4 096 символов.

Фото и видео в одном сообщении: до 10 штук.

Объём отправляемых файлов: немного больше 2 ГБ.

Длина имени файла: до 60 символов.

Описание к медиафайлам: до 1 024 символов.

Длительность видеособщения: до 1 минуты.

Планирование сообщений: до 365 дней.

Количество отложенных сообщений: до 100 сообщений.

Как создать пост в Telegram?
ЭКСКЛЮЗИВЫ — ЧИТАЙТЕ ТОЛЬКО В БЛОГЕ UNISENDER
Кейс Unisender и «Понимаю»: быстрый переезд на новый сервис рассылок без потери базы
CRM-маркетинг в НКО «ЖИВИ»
5 странных требований заказчиков
Нужно ли любить свой продукт
Продвижение без бюджета. А что, так можно было?
Чаты и группы
Чаты и группы в Telegram предназначены для общения. Все участники могут участвовать в общей переписке, обмениваться аудиосообщениями, пересылать медиафайлы и документы. Для чатов и групп также предусмотрены лимиты:

Число участников группы: до 200 000 человек. 

Число участников голосового чата: до 5 000 человек. 

Длина названия: 5–32 символа.

Длина описания группы: до 255 символов. 

Длина названия чата: до 128 символов. 

Длина @username для группы: 5–32 символов. 

Длина сообщения в чате или группе: до 4 096 символов. 

Описание к медиафайлам: до 1 024 символов. 

Объём передаваемых файлов: до 2 ГБ. 

Длина видеособщений: до 1 минуты. 

Количество фото в одном сообщении: до 10 штук. 

Доступность редактирования сообщений в личных чатах: до 48 часов. 

Количество упоминаний пользователей в одном сообщении: до 50 аккаунтов. 

Настройка самоуничтожения фото и видео в личных чатах: от 1 до 60 секунд. 

Количество видимых сообщений в группе: до 1 000 000. 

Количество закреплённых сообщений: неограниченно. 

Количество единовременно пересылаемых сообщений: до 100. 

Количество приглашений в группу (инвайтов): до 200 человек. 

Количество администраторов в группе: до 50 человек. 

Количество ботов, подключенных к группе: до 20. Кстати, в блоге Unisender есть обзор 15 полезных ботов для ведения каналов и чатов в Telegram.

Открытие статистики: для сообществ от 100 человек. 

История действий участников: за последние 2 дня. 

Преобразование супергруппы в группу для трансляций: для чатов с числом участников от 199 000 человек.
'''

# clients = []

# def start_bot(clients_list):
#     global clients
#     clients = clients_list

# def show():
#     print(clients)

# show()
# start_bot('ggg')
# show()


# d = datetime.datetime.now()

# print(d.strftime("%m-%d, %H:%M"))


# from multiprocessing import Process, Event
# from time import sleep

# event = Event()

# def a(event):
#     while True:
#         event.wait()
#         print(123)
#         sleep(1)
#         event.clear()
    

# if __name__ == '__main__':
#     Process(target=a, args=(event,)).start()
#     Process(target=a, args=(event,)).start()
#     print('Начинаем')
#     sleep(3)
#     event.set()
#     sleep(10)



# async def procces():
#     while True:
#         print('Ожидаем события')
#         await event.wait()
#         print('Код что-то обрабатывает')
#         await asyncio.sleep(1)
#         event.clear()


# async def procces_true():
#     while True:
#         event.set()
#         await asyncio.sleep(5)


# loop = asyncio.get_event_loop()
# loop.create_task(procces())
# loop.create_task(procces_true())
# loop.run_forever()

# import asyncio

# event = asyncio.Event()

# async def aaa():
#     await event.wait()
#     event.clear()
#     print('Холоп')

# async def bbb():
#     await aaa()
#     event.set()


# asyncio.run(bbb())


# from random import randint


# stickers_sets = {
#     'ValentineCat': 5,
#     'MrCat': 2,
#     'TidyTieTom': 5,
#     'DolphinDolph': 5,
#     'HotCherry': 5,
# }


# # Берем рандомный стикер
# len_set = len(stickers_sets)
# rand_var = randint(1, len_set)
# key = 1

# for name, number in stickers_sets.items():
#     if rand_var != key:
#         key += 1
#     else:
#         break

# print(name, number)


# from clients import config
# from loader import db


# users_blacklist = [usr[0] for usr in db.fetchall('SELECT username FROM blacklist')]
# # user = users.pop(0)
# user = '@gelya_lina_o'

# # Сразу добавляем пользователя в базу, чтобы не было двойной отправки
# db.query('INSERT OR IGNORE INTO blacklist VALUES (?)', (user,)) 

# # Проверка пользователя в блэклисте
# if user in users_blacklist:
#     print(f'уже отправляли сообщение этому пользователю | {user} |')



# from loader import db

# clients_list = {
#     'Тест 4': 'client4',
#     'Тест 5': 'client5',
#     'Тест 6': 'client6'
# }


# accounts = {account[0]:clients_list[account[0]] for account in db.fetchall('SELECT * FROM accounts WHERE status = "готов"')}

# print(accounts)

# from time import sleep

# from clients import config
# from loader import db

# while True:
#     # if len(users) > 0: # Если в списке остались пользователи
#     if config.count_spam_user() > 0:
#         # Достаем черный список из базы и проверяем есть ли пользователь в нем, есди да берем следующего пользователя
#         users_blacklist = [usr[0] for usr in db.fetchall('SELECT username FROM blacklist')]
#         # user = users.pop(0)
#         user = config.get_spam_user()

#         # Сразу добавляем пользователя в базу, чтобы не было двойной отправки
#         db.query('INSERT OR IGNORE INTO blacklist VALUES (?)', (user,)) 
        
#         # Проверка пользователя в блэклисте
#         if user in users_blacklist:
#             print(f'уже отправляли сообщение этому пользователю | {user} |')
#             continue

#         print(f'Отправляем сообщение {user}')
        
#         sleep(1)
            

# from clients import config
# from loader import db


# spam_users = [user[0].strip() for user in db.fetchall('SELECT * FROM blacklist')]

# db.query('DELETE FROM blacklist')

# for spam_user in spam_users:
#     db.query('INSERT OR IGNORE INTO blacklist VALUES (?)', (spam_user,))


# # Подсчет всех отправленных сообщений сообщений
# def save_count_send_messages(send_users: int):
#     with open(file='logs.txt', mode='r', encoding='UTF-8') as fl:
#         text = fl.read()
#         if text == '':
#             text = send_users
#         else:
#             text = int(text) + send_users
            

#     with open(file='logs.txt', mode='w', encoding='UTF-8') as fl:
#         fl.write(str(text))



# save_count_send_messages(10)


# import asyncio


# async def foo(val):
#     value = 0
#     while True:
#         value += 1
#         print(f'| {val} | Работаю не покладая рук')
#         await asyncio.sleep(2)
        
#         if value == 3:
#             asyncio.tasks.current_task().cancel()
#             print(f'| {val} | Закрыл')
#             loop.create_task(boo())
#             await asyncio.sleep(1)


# async def boo():
#     while True:
#         print('Я тоже работаю, но пореже')
#         await asyncio.sleep(3)


# loop = asyncio.get_event_loop()

# loop.create_task(foo(1))
# # loop.create_task(boo())

# loop.run_forever()


# from zipfile import ZipFile
# import os
# import shutil


# a = 'accounts.zip'

# with ZipFile(file=a, metadata_encoding='cp866') as file_zip:
#     file_zip.extractall(path='test_zip_file_extract')


# folders_tdata = os.listdir('accounts')

# path_to_tdata = {}
# for folder_tdata in folders_tdata:
#     path = os.path.join('accounts', folder_tdata, 'tdata')

#     if os.path.isdir(path):
#         path_to_tdata[folder_tdata] = path
#     else:
#         print(f'Папка tdata не найдена, удаляю дирректорию | {folder_tdata} |')
#         shutil.rmtree(path=os.path.join('accounts', folder_tdata))

# from loader import db
# from datetime import datetime

# info = ''

# accounts = db.fetchall('SELECT * FROM accounts WHERE status = ?', ('спам',))
# info += f'\n\n🔹 <b>В СПАМ БЛОКЕ | {len(accounts)} |</b>'
# for account in accounts:
#     time_info = datetime.now() - datetime.fromisoformat(account[4])

#     info += f'\n ┠ {account[0]} | в спам блоке, прошло | {time_info.days} д. {round(time_info.seconds / 60 / 60, 1)} ч. |'
#     print(info)


# def numbers_in_emoji(numbers: int):
#     emoji = ('0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣')

#     msg = ''
#     for number in str(numbers):
#         if number == '0': msg += emoji[0]
#         if number == '1': msg += emoji[1]
#         if number == '2': msg += emoji[2]
#         if number == '3': msg += emoji[3]
#         if number == '4': msg += emoji[4]
#         if number == '5': msg += emoji[5]
#         if number == '6': msg += emoji[6]
#         if number == '7': msg += emoji[7]
#         if number == '8': msg += emoji[8]
#         if number == '9': msg += emoji[9]


#     return msg





# from clients import accounts_manager
# from tools import numbers_in_emoji



# new_accounts = accounts_manager.get_unique_id_by_status('новый')
# prep_accounts = accounts_manager.get_unique_id_by_status('прогрев')
# after_spam_accounts = accounts_manager.get_unique_id_by_status('отлежка')
# spam_block_accounts = accounts_manager.get_unique_id_by_status('спам')

# # Присваиваем порядковые номера и аккаунтам и формируем строку
# text = ''
# number = 0



# text += '<b>НОВЫЕ</b>\n'
# for account in new_accounts:
#     number += 1
#     text += numbers_in_emoji(number)
#     text += f' {account}\n'

# text += '\n<b>ПРОГРЕВ</b>\n'
# for account in prep_accounts:
#     number += 1
#     text += numbers_in_emoji(number)
#     text += f' {account}\n'

# text += '\n<b>ОТЛЕЖКА</b>\n'
# for account in after_spam_accounts:
#     number += 1
#     text += numbers_in_emoji(number)
#     text += f' {account}\n'

# text += '\n<b>СПАМ</b>\n'
# for account in spam_block_accounts:
#     number += 1
#     text += numbers_in_emoji(number)
#     text += f' {account}\n'



# print(text)





# all_accounts = ['Тест 1', '24', '23', 'Тест 2']

# text = '2 3'


# edit_accounts = []
# if '-' in text:
#     text_split = text.strip().split('-')
#     try:
#         number_1 = int(text_split[0])
#         number_2 = int(text_split[1])
    
#         edit_accounts = all_accounts[number_1 - 1:number_2]
#     except Exception:
#         pass

# else: 
#     text_split = text.strip().split(' ')
    
#     for acc_index in text_split:
#         try:
#             edit_accounts.append(all_accounts[int(acc_index) - 1])
#         except Exception:
#             pass


# print(edit_accounts)


# from loader import db


# db.query('ALTER TABLE config ADD count_send_msg INT DEFAULT 0')




# import logging



# # Создали логгер
# logger = logging.getLogger(name='Spam_Info')
# logger.setLevel(level='INFO')

# # Создали обработчик для записи в файл
# file_handler = logging.FileHandler(filename='logs.txt', encoding='utf-8')
# # Настроили формат вывода данных для обработчика
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# # Создали обработчик вывода в консоль
# strim_handler = logging.StreamHandler()

# # Привязали обработчик
# logger.addHandler(file_handler)
# logger.addHandler(strim_handler)



# logger.info('привет')



# def error_handler(func):
#     def other_func(*args, **kwargs):
#         try:
#             func(*args, **kwargs)
#         except ZeroDivisionError:
#             print('На ноль делить нельзя')
    
#     return other_func


# @error_handler
# def main_func(a, b, c):
#     print(f'Поделил = {a/b}')
#     print(f'Это третий аргемент {c}')



# from loader import db

# phones = '''
# 79273453888
# 79209782502
# 79853644164
# 79132512632
# 79776258829
# 79537391693
# 79951084808
# 79875802099
# 79819833731
# 79521270001
# 79780774612
# 79521265898
# 79105097573
# 79057289838
# 79818155558
# 79106435546
# 79206360770
# 79052112334
# 79998397028
# 79209644768
# 79525968809
# 79604603500
# 79508081030
# 79805627725
# 79133250272
# 79109015591
# 79195378879
# 79105724000
# 79109022175
# 79104643943
# 79036938651
# 79532347870
# 79209565944
# 79206334488
# 79065464286
# 79189595447
# 79772703437
# 79156152484
# 79106418372
# 79622935255
# 79009042672
# 79065433304
# 79859855105
# 79588665454
# 447976489267
# 79277159455
# 79105772806
# 79537087096
# 79106418069
# 79105764396
# 79095522244
# 79521214376
# 79028814065
# 79106244242
# 79521204400
# 79661178889
# 79620363864
# 79156062046
# 79537399419
# 79521221199
# 79537355456
# 79119292404
# 79156170111
# 79036414377
# 79106420023
# 79046565753
# 79106283934
# 79883321108
# 79056931355
# 79109013606
# 79209971201
# 79209673419
# 79109046339
# 79537311124
# 79150559328
# 79038362000
# 79206358780
# 79109050662
# 79679009130
# 79057316665
# 79805629069
# 79105628870
# 79995210181
# 79156261464
# 79029273023
# 79105006440
# 79165718459
# 79537326798
# 79109001630
# 79106142104
# 79056909096
# 79209744179
# 79106231289
# 79006090425
# 79006022810
# 79106102436
# 79106111740
# 79883441277
# 79209821245
# 79166526006
# 79209758741
# 79150587751
# 79588669896
# 79036406621
# 79066465359
# 79015983843
# 79106310751
# 79206306310
# 79657134472
# 79150186833
# 79081783060
# 79064268913
# 79006067764
# 79831549835
# 79038370713
# 79105714833
# 79965724998
# 79156211060
# 79105093260
# 79912295019
# '''

# for phone in phones.strip().split('\n'):
#     db.query('INSERT OR REPLACE INTO phones VALUES (?)', (phone,))



# transliteration_data = {
#     'А': 'A', '	Б': 'B', 'В': 'V',
#     'Г': 'G', 'Д': 'D', 'Е': 'E',
#     'Ё': 'JO', 'Ж': 'ZH', 'З': 'Z',
#     'И': 'I', 'Й': 'JJ', 'К': 'K',
#     'Л': 'L', 'М': 'M', 'Н': 'N',
#     'О': 'O', 'П': 'P', 'Р': 'R',
#     'С': 'S', 'Т': 'T', 'У': 'U',
#     'Ф': 'F', 'Х': 'KH', 'Ц': 'C',
#     'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHH',
#     'Ы': 'Y', 'Э': 'EH', 'Ю': 'JU',
#     'Я': 'JA'
# }


# def transliteration_str(text: str) -> str:
#     text = text.strip().upper()
#     print(text)
#     translit_text = ''
#     for symbol in text:
#         if symbol in transliteration_data.keys():
#             translit_text += transliteration_data[symbol]
    
#     return translit_text.lower()


# print(transliteration_str('Привет! sds ваквува прапа ✅'))


# a = 'A B C D E F G H I K L M N O P Q R S T V X Y Z'

# a = a.lower()
# b = (symbol for symbol in a.split(' '))
# print(tuple(b))



# from loader import db


# with open(file='data/entities/bio.txt', mode='r', encoding='utf-8') as f:
#     bio_sss = f.read()


# for bio in bio_sss.split('\n'):
#     print(bio)
#     db.query('INSERT OR REPLACE INTO bio VALUES (?)', (bio,))

# import os
# import shutil
# from zipfile import ZipFile


# with ZipFile(file='test_zip.zip', metadata_encoding='cp866') as file_zip:
#     files_names = file_zip.namelist()
#     files = []
#     for file_name in files_names:
#         if file_name.find('key_datas') != -1 or file_name.find('D877F783D5D3EF8Cs') != -1 or file_name.find('maps') != -1:
#             files.append(file_name)

#     file_zip.extractall(path='test_zip', members=files)




# dirs = os.listdir('test_zip')
# for dir in dirs:
#     print(dir)
#     dirs_2 = os.listdir(os.path.join('test_zip', dir))
#     print(dirs_2)




# def error_handler(func):
#     def other_func(*args, **kwargs):
#         try:
#             func(*args, **kwargs)
#         except ZeroDivisionError:
#             print('На ноль делить нельзя')
    
#     return other_func




# import asyncio
# from random import randint


# def excp(func):
#     async def wrapped(*args, **kwargs):
#         try:
#              await func(*args, **kwargs)
#         except asyncio.exceptions.CancelledError:
#             return
    
#     return wrapped

        

# class Test():
#     def __init__(self) -> None:
#         pass
    
#     @excp
#     async def aaa(self, info):
#         while True:
#             print(info)
#             await asyncio.sleep(1)
            

# async def aaa_stop(tasks, time):
#     await asyncio.sleep(time)
#     for task in tasks:
        
#         print(a)
#         name = task.get_name()
#         print(f'Завершаю подпрограмму {name}')
#         task.cancel()


# async def main():
#     tasks = []
#     tasks2 = []
#     rr = Test()
#     for a in range(5):
#         tasks.append(loop.create_task(rr.aaa(a)))

#     # for b in range(5):
#     #     tasks2.append(loop.create_task(rr.aaa(f'2 -- | {a} |')))
    
    
#     loop.create_task(aaa_stop(tasks, 3))
#     # loop.create_task(aaa_stop(tasks2, 5))



#     await asyncio.gather(*tasks)
#     print('Завершил')
#     # await asyncio.gather(*tasks2)
#     # print('Завершил')





# loop = asyncio.get_event_loop()
# a = loop.create_task(main())
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     print('СТОП')


# from clients import links_manager


# message = '[@PostBot 65fa36561ccfa]'

# print(message[:-1])


# if message[:5] == 'https':
#     messgae_split_space = message.split(' ')
#     if len(messgae_split_space) == 1:
#         message_split = message.split('/')
#         msg_id = message_split[4]
#         link = f'{message_split[0]}//{message_split[2]}/{message_split[3]}/'
#         links_manager.insert_link(link=link, msg_id=int(msg_id), count_msg=200)

#     if len(messgae_split_space) == 2:
#         message_split = messgae_split_space[0].split('/')
#         msg_id = message_split[4]
#         link = f'{message_split[0]}//{message_split[2]}/{message_split[3]}/'
#         links_manager.insert_link(link=link, msg_id=int(msg_id), count_msg=int(messgae_split_space[1]))

# if message[:6] == '[@Post':
#     messgae_split_space = message.split(' ')
#     if len(messgae_split_space) == 2:
#         links_manager.insert_link(link=messgae_split_space[0], msg_id=messgae_split_space[1], count_msg=200)

#     if len(messgae_split_space) == 3:
#         links_manager.insert_link(link=messgae_split_space[0], msg_id=messgae_split_space[1], count_msg=int(messgae_split_space[2]))



# from telethon.network.connection import connection

from loader import db

db.query('ALTER TABLE config ADD spam_delay TEXT DEFAULT "10 30"')
