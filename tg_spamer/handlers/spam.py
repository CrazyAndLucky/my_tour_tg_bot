import asyncio
from random import randint, randrange
from datetime import datetime
import logging

from opentele.tl import TelegramClient
from telethon import errors
from telethon.tl.functions.messages import SetTypingRequest, GetStickerSetRequest, GetInlineBotResultsRequest
from telethon.tl.functions.channels import GetParticipantsRequest, JoinChannelRequest
from telethon.tl.functions.contacts import AddContactRequest
from telethon.types import ChannelParticipantsSearch, SendMessageRecordAudioAction, SendMessageTypingAction, InputStickerSetShortName, SendMessageChooseStickerAction
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError

from tg_spamer.loader import db
from tg_spamer.config import get_message, stickers_sets
from tg_spamer.clients import config, links_manager, accounts_manager



logger = logging.getLogger(name='Spam_Info')


async def spammer(user_b: list, client: TelegramClient, unique_id, send_message: bool = None, link: bool = None, postbot: bool = None, voice: bool = None, dual_send: bool = None):
    account = accounts_manager.get_acc_info_by_unique_id(unique_id=unique_id)
    if account[3] == 'готов' or account is None:
        # await asyncio.sleep(config.delay())
        spam_block = False
        count_message = account[6]
        send_users = 0 
        send_messages_users = [] # Пользователи которым отправили сообщение
        try:
            account_phone = (await client.get_me()).phone
            random_time = round(count_message / 2, 0) # Когда сделать рандомное действие 

            while True:
                # if len(users) > 0: # Если в списке остались пользователи
                # if config.count_spam_user() > 0:
                if len(user_b) > 0:
                    # users_blacklist = [usr[0] for usr in db.fetchall('SELECT username FROM blacklist')]
                    user = user_b.pop()
                    
                    # # Проверка пользователя в блэклисте
                    # if user in users_blacklist:
                    #     print(f'| {unique_id} | уже отправляли сообщение этому пользователю | {user} |')
                    #     continue


                    try: 
                        # Проверка на блок от пользователя
                        status = await process_check_users(client, send_messages_users, unique_id)
                        if status == 'STOP':
                            save_count_send_messages(unique_id, send_users)
                            break
                        
                        # Рандомное действие
                        if send_users == random_time:
                            await random_action(client, unique_id)    

                        # Давойная отправка
                        if dual_send:
                            rand_send = randint(0, 3)
                            if rand_send == 1:
                                message = await msg(unique_id, user, client, prep_message=True)
                                if message is None:
                                    continue

                                # rand_var = randint(0, 1)
                                rand_var = 1
                                if rand_var == 0:
                                    await client(SetTypingRequest(peer=user, action=SendMessageTypingAction()))
                                    await asyncio.sleep(2)
                                    await client.send_message(entity=user, message=message)
                                    await asyncio.sleep(5)

                                else: 
                                    # Берем рандомный стикер из списка
                                    len_set = len(stickers_sets)
                                    rand_var = randint(1, len_set)
                                    key = 1

                                    for name, number in stickers_sets.items():
                                        if rand_var != key:
                                            key += 1
                                        else:
                                            break
                                    
                                    # Отправляем стикер
                                    sticker_set = await client(GetStickerSetRequest(stickerset=InputStickerSetShortName(short_name=name), hash=0))
                                    await client(SetTypingRequest(peer=user, action=SendMessageChooseStickerAction()))
                                    await asyncio.sleep(2)
                                    await client.send_file(entity=user, file=sticker_set.documents[number - 1])
                                    await asyncio.sleep(5)
                        
                        
                        # Рассылка войса
                        if voice:
                            # results = await client.inline_query(bot='@PostBot', query='65fa36561ccfa', entity=user)
                            # await results[0].click()
                            await client(SetTypingRequest(peer=user, action=SendMessageRecordAudioAction()))
                            await asyncio.sleep(1)
                            await client.send_file(entity=user, file='data/voice.mp3', voice_note=True)

                        
                        # Расслка сообщения с кнопкой через postbot
                        if postbot:
                            link_base = links_manager.get_one_link_postbot()
                            
                            if link_base:
                                query = link_base[2]

                                results = await client.inline_query(bot='@PostBot', query=query, entity=user)
                                await results[0].click()
                                links_manager.decrease_count_msg(link_base[0])
                            
                            else:
                                logger.info(f'| {unique_id} | ссылки закончлись')
                                save_count_send_messages(unique_id, send_users)
                                config.insert_spam_user(user) # Так как пользователю не отправили сообщение добавляем его обратно в базу :)
                                break
                        
                        
                        # Расслка сообщения с кнопкой
                        if link:
                            link_base = links_manager.get_one_link()
                            
                            if link_base:
                                msg_id = link_base[2]
                                link_chat = link_base[1]
                                
                                # Отправили сообщение спам-юзеру
                                await client.forward_messages(entity=user, messages=msg_id, from_peer=link_chat)
                                # Умешьшаем кол-во сообещние доступных для ссылки
                                links_manager.decrease_count_msg(link_base[0])
                            
                            else:
                                logger.info(f'| {unique_id} | ссылки закончлись')
                                save_count_send_messages(unique_id, send_users)
                                config.insert_spam_user(user) # Так как пользователю не отправили сообщение добавляем его обратно в базу :)
                                break

                        
                        # Рассылка текстового сообщения
                        if send_message:
                            message = await msg(unique_id, user, client)
                            if message is None:
                                continue

                            await client(SetTypingRequest(peer=user, action=SendMessageTypingAction()))
                            await asyncio.sleep(2)
                            await client.send_message(entity=user, message=message)
                            await client.send_read_acknowledge(entity=user)


                        # Добавляем пользователя в блэклист
                        db.query('INSERT OR IGNORE INTO blacklist VALUES (?)', (user,)) 

                        # Подсчитываем кол-во сообщений
                        send_users += 1
                        logger.info(f'| {unique_id} | сообщение | #{send_users} |  успешно отправленно | {user} |')
                        if send_users == count_message:
                            save_count_send_messages(unique_id, send_users)
                            break
                        
                        
                        # Рандомный дисконнект
                        remains = send_users % randrange(6, 9, 2)
                        if remains == 0:
                            print(f'| {unique_id} | отключается')
                            await client.disconnect()
                            await asyncio.sleep(delay=config.delay())
                            print(f'| {unique_id} | полдключается')
                            await client.connect()
                            await asyncio.sleep(6)

                        # Задержка
                        await asyncio.sleep(delay=config.delay())


                    # Обработка ошибок
                    except errors.FloodError as e:
                        logger.info(f'| {unique_id} | флуд {e.seconds} отправленно сообщений: {send_users}')
                        spam_block = True
                        save_count_send_messages(unique_id, send_users)
                        # users.insert(0, user)
                        config.insert_spam_user(user) # Так как пользователю не отправили сообщение добавляем его обратно в базу :)
                        break

                    except errors.PeerFloodError as e:
                        print(e)
                        logger.info(f'| {unique_id} | в спам блоке, отправленно сообщений: {send_users}')
                        spam_block = True
                        save_count_send_messages(unique_id, send_users)
                        # users.insert(0, user)
                        config.insert_spam_user(user)
                        break

                    except ConnectionError:
                        print(f'| {unique_id} | потеряно соединение')
                        print('попытска дисконнекта')
                        await client.disconnect()
                        await asyncio.sleep(7)

                        # Через несколько чекунд пробуем ещё раз присоединиться
                        try:
                            await client.connect()
                             # Проверка аккаунта на бан
                            me = await client.get_me()
                            if me is None:
                                logger.info(f'Аккаунт забанен | {unique_id} |')

                        except TypeError:
                            print(f'| {unique_id} | проблема с прокси')
                            await client.disconnect()
                            
                            save_count_send_messages(unique_id, send_users)
                            config.insert_spam_user(user) # Добавялем пользвоателя обратно в базу, так как ему сообщение не отправилось
                            break

                        except ConnectionError:
                            print(f'| {unique_id} | проблема с прокси или с сетью')
                            await client.disconnect()
                            
                            save_count_send_messages(unique_id, send_users)
                            config.insert_spam_user(user) # Добавялем пользвоателя обратно в базу, так как ему сообщение не отправилось
                            break
                        
                        except AuthKeyDuplicatedError:
                            print(f'| {unique_id} | ошибка авторизации, аккаут выбило, удаляю')
                            await client.log_out()

                            save_count_send_messages(unique_id, send_users)
                            config.insert_spam_user(user) # Добавялем пользвоателя обратно в базу, так как ему сообщение не отправилось
                            break

                    except errors.ForbiddenError:
                        logger.info(f'| {unique_id} | пользователь | {user} |  запретил отпарвку ему текстовых сообщений')
                        await asyncio.sleep(15)
                    
                    except errors.VoiceMessagesForbiddenError:
                        logger.info(f'| {unique_id} | пользователь | {user} |  запретил отпарвку ему голосовых и видео')
                        await asyncio.sleep(15)

                    except ValueError:
                            print(f'| {unique_id} | такого пользователя нет | {user} |')

                
                else:
                    logger.info(f'| {unique_id} | пользователи закончились')
                    save_count_send_messages(unique_id, send_users)
                    break
            
            logger.info(f'| {unique_id} | завершил работу, отправленно сообщений: {send_users}')
            if spam_block:
                accounts_manager.post_acc(unique_id=unique_id, status='спам', time=datetime.now(), messages=config.update_msg(unique_id, -5))
            else:
                accounts_manager.post_acc(unique_id=unique_id, status='отлежка', time=datetime.now(), messages=config.update_msg(unique_id, 3))

        except ConnectionError:
            logger.info(f'| {unique_id} | аккаунт забанен, отправленно сообщений: {send_users}')
            save_count_send_messages(unique_id, send_users)

    else: 
        pass


# Получаем сообщение
async def msg(unique_id, user, client: TelegramClient, prep_message=None):
    if prep_message is None:
        message = get_message()
    else:
        message = get_message(prep_message=True)

    # Вставляем в сообщение имя, если нужно
    name = message.find('[имя]')
    if name != -1:
        try:
            user_info = await client.get_entity(entity=user)
            message = message.replace('[имя]', user_info.first_name)
            return message

        except ValueError:
            print(f'| {unique_id} | пользователь | {user} | не существует')
            return None


# Подсчет всех отправленных сообщений сообщений
def save_count_send_messages(unique_id, send_users: int):
    # Сохраняем кол-во отправленных сообщений аккаунтов
    print(f'| {unique_id} | сохранил, кол-во отправленных сообщений {send_users}')
    accounts_manager.post_acc(unique_id=unique_id, spam_messages=send_users)
    # Сохраняем общее кол-во отправленных сообщений
    config.increase_count_send_msg(count_msg=send_users)


# Проверка на блокировку от пользователя
async def process_check_users(client: TelegramClient, send_messages_users: list, unique_id):
    for send_message_user in send_messages_users:
        message_in_dialog = await client.get_messages(entity=send_message_user, limit=1)
        if not message_in_dialog:
            logger.info(f'| {unique_id} | завершил работу так как пользователь: | {send_message_user} | вероятно заблокировал аккаунт')
            return 'STOP'


# Случайное действие
async def random_action(client: TelegramClient, unique_id):
    print(f'| {unique_id} | выполняю рандомное действие')
    chanels = list((chanel[0] for chanel in db.fetchall('SELECT * FROM chanels')))
    while True:
        try:
            # Рандомный канал
            chanel = chanels[randint(0, len(chanels) - 1)]
            chanel_info = await client.get_entity(entity=chanel)
            
            # Читаем последние 5 постов
            messages = await client.get_messages(chanel_info, 5)
            await client.send_read_acknowledge(entity=chanel_info, message=messages)
            await asyncio.sleep(8)
            
            # Подписываемся на канал
            await client(JoinChannelRequest(channel=chanel_info))
            print(f'| {unique_id} | подписался на канал | @{chanel_info.username} |')
            await asyncio.sleep(8)
            break

        except ConnectionError:
            print('Нет соединения')
            pass    

        except Exception as e:
            print(f'| {unique_id} | ошибка с каналом: {e}')
            continue


async def get_messages_for_forward(client: TelegramClient, unique_id, link: int, chat):
    await client.forward_messages(entity='me', messages=link, from_peer=chat)
