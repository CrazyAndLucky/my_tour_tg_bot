# import logging
import asyncio



# logger = logging.getLogger(name='Spam_Info')


def errors_handler_client(func):
    async def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ConnectionError:
            print('Нет соединения')

    return wrapped


def errors_loop(func):
    async def wrapped(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except asyncio.exceptions.CancelledError:
            print('Завершил коррутину')
            return
        
    return wrapped