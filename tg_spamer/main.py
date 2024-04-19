import logging

from tg_spamer.bot import bot_main, event_update
from tg_spamer.clients import loop
from tg_spamer.functions import acc_info


logger = logging.getLogger(name='Spam_Info')
logger.setLevel(level='INFO')
file_handler = logging.FileHandler(filename='tg_spamer/logs.txt', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# strim_handler = logging.StreamHandler()
logger.addHandler(file_handler)
# logger.addHandler(strim_handler)


def tg_spamer_start():

    loop.run_until_complete(acc_info(connect=False))

    menu_text = '\n=======================\n'
    menu_text += '-- ПРОВЕРИТЬ АККАУНТЫ: чек\n'
    menu_text += '-- ПОМЕНЯТЬ ИМЯ: имя\n-- ПОМЕНЯТЬ ФОТО: фото\n-- ПОМЕНЯТЬ БИО: био\n'
    menu_text += '-- ПРОГРЕТЬ АККАУНТЫ: прогрев\n-- ПОМЕНЯТЬ СТАТУС С НОВЫХ НА ГОТОВЫЕ: готов\n'
    menu_text += '-- РАССЫЛКА ВОЙСА ИЛИ КРУЖКА С КНОПКОЙ: кружок\n-- РАССЫЛКА ТЕКСТА: текст\n'
    menu_text += '-- РАССЫЛКА ТЕКСТА С ОЖИДАНИЕМ: текст+\n'
    menu_text += '-- РАССЫЛКА ВОЙСА С ОЖИДАНИЕМ: войс\n'
    menu_text += '-- ЗАПУСТИТЬ ТОЛЬКО РЕЖИМ ПРИЕМА СООБЩЕНИЙ: бот\n-- УПРАВЛЕНИЕ ЧЕРЕЗ БОТА: бот+'
    print(menu_text)


    # flag = input('\n').lower()
    flag = 'бот+'

    if flag == 'кружок' or flag == 'текст' or flag == 'войс':
        flag_2 = input('ДЕЛАТЬ ДВОЙНУЮ ОТПРАВКУ: (1 - да, 0 - нет): ')
    else:
        flag_2 = 0

    try:
        if flag == 'текст+' or flag == 'бот' or flag == 'войс':
            event_update.set()
            # loop.create_task(bot_main())

            # loop.create_task(main(flag, flag_2))
            loop.run_forever()
        elif flag == 'бот+':
            # loop.create_task(bot_main())
            # loop.create_task(start_forward_m())
            # loop.create_task(loop_update_accounts_info())
            # loop.create_task(loop_check_connect())
            loop.run_forever()
        else: 
            # loop.run_until_complete(main(flag, flag_2))
            print('\n=======================\nВЫПОЛНИЛ')
    except KeyboardInterrupt:
        print('STOP')