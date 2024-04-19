import asyncio

from opentele.tl import TelegramClient
from telethon.tl.functions.messages import SetTypingRequest, GetStickerSetRequest
from telethon.types import ChannelParticipantsSearch, SendMessageTypingAction, SendMessageRecordAudioAction, InputStickerSetShortName, SendMessageChooseStickerAction
from telethon.tl.custom.message import Message

from tg_spamer.clients import clients_list


# Пишет пользователю
async def send_msg_to_user(unique_id, text, user_id):
    client: TelegramClient = clients_list[unique_id]

    '''Тест отправки стикера'''
    # 1 вариант
    # all_stickers_in_account = await client(GetAllStickersRequest(0))
    # sticker_set = await client(GetStickerSetRequest(stickerset=InputStickerSetID(id=all_stickers_in_account.sets[0].id, access_hash=all_stickers_in_account.sets[0].access_hash), hash=0))
    # await client(SetTypingRequest(peer=user_id, action=SendMessageChooseStickerAction()))
    # await asyncio.sleep(2)
    # await client.send_file(entity=user_id, file=sticker_set.documents[0])

    # 2 вариант
    # sticker_set = await client(GetStickerSetRequest(stickerset=InputStickerSetShortName(short_name='c6fea417_7e25_421d_963d_65cc90d62d12_by_sticat_bot'), hash=0))
    # await client(SetTypingRequest(peer=user_id, action=SendMessageChooseStickerAction()))
    # await asyncio.sleep(2)
    # await client.send_file(entity=user_id, file=sticker_set.documents[0])


    '''Тест отправки голосового сообщения'''
    # await client(SetTypingRequest(peer=user_id, action=SendMessageRecordAudioAction()))
    # await client.send_file(entity=user_id, file='data/voice.mp3', voice_note=True)



    # Отправяляем сообщение пользователю
    await client.send_read_acknowledge(entity=user_id)
    await asyncio.sleep(1)
    await client(SetTypingRequest(peer=user_id, action=SendMessageTypingAction()))
    await asyncio.sleep(3)
    await client.send_message(entity=user_id, message=text)
    print(f'| {unique_id} | отправил сообщение пользователю | {user_id} |')


# Удалить дилог у себя и у спам-юзера
async def delete_dialog(unique_id, user_id):
    client: TelegramClient = clients_list[unique_id]

    await client.delete_dialog(entity=user_id, revoke=True)


# Прочитать сообщения спам-юзера
async def send_read_messages(unique_id, user_id):
    client: TelegramClient = clients_list[unique_id]

    await client.send_read_acknowledge(entity=user_id)


async def forward_message():
    unique_id = 'Тест'

    client: TelegramClient = clients_list[unique_id]

    await client.connect()
    await client.forward_messages(entity='https://t.me/K_Yu_P', messages=10, from_peer='https://t.me/cfgfdgfdgf4443fd')



# Получить медиа
async def get_media_from_msg(unique_id, user_id, message_id):
    client: TelegramClient = clients_list[unique_id]

    message = await client.get_messages(user_id, ids=message_id)
    
    media = await client.download_media(message, file=bytes)
    
    return media