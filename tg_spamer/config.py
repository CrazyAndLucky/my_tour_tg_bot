from random import randint


# Сообщения для рассылки
message_text = [
'''
[имя], привет! Мы с тобой вместе принимали участие в новогоднем марафоне...
''',
]


prep_message_text = [
'''ы
[имя], Привет! 
''',
'''
Привет, [имя]!  
''',
]


stickers_sets = {
    'ValentineCat': 4,
    'MrCat': 2,
    'TidyTieTom': 5,
    'DolphinDolph': 5,
    'HotCherry': 5,
    'SnowManul': 5,
    'HappyHippos': 5,
    'CatInHat': 5,
    'Animals': 1,
    'Animals': 2,
    'Animals': 3,
    'Animals': 4,
    'Animals': 5,
    'GrinchDog': 5,
    'UtyaD': 5,
    'ElPablo': 5,
    'ArmBirds': 3,
    'BirdOfParadise': 5,
    'PenguinsLoloPepe': 5,
    'Cockatoo': 5, 
    'GagikTheDuck': 5,
    'DodoBird': 5,
    'Kiwi_Kiwi': 5,
    'FreakyPigeon': 5,
    'PoolFlamingo': 5,
    'ScreamingChicken': 5,
    'OfficeTurkey': 5,
    'DetectiveCaplini': 5,
}


# Ид чата для перессылки, юзернейм и токен перессыльного бота 
chat_id = '-1001927560575'


# Начальное вол-во сообщений для новых аккаунтов
start_count_messages = 5


# Задержка между сообщениями
# def delay() -> int:
#     delay = randint(10, 30)

#     return delay


##############################################################################
##############################################################################

message_randomize = {
    'А': 'A',
    'В': 'B',
    'С': 'C',
    'Е': 'E',
    'Н': 'H',
    'К': 'K',
    'М': 'M',
    'О': 'O',
    'Р': 'P',
    'Т': 'T',
    'Х': 'X',
    'а': 'a',
    'с': 'c',
    'е': 'e',
    'о': 'o',
    'р': 'p',
    'х': 'x',
}


# Рандомизация текста
def randomize_text(text):
    end_message = ''
    for symbol in text:
        # Рандомизируем символы
        for values in message_randomize.items():
            if symbol in values:
                symbol = values[randint(0, 1)]

        # Собираем сообщение заного
        end_message += symbol
    
    return end_message


# Сообщение для рассылки
def get_message(prep_message=None) -> str:
    flag = 0 # Включить и выклюить подбор в скобках {}
    msg = '' # Сбор одного сообщения в скобках {}
    end_message = ''

    if prep_message is None:
        message = message_text
    else:
        message = prep_message_text

    
    # Бежим по каждому символу и выделяем то что в скобках и рандомизируем текст
    for symbol in message[randint(0, len(message)) - 1]:
        if symbol == '{':
            flag = 1
            continue # Он не добавит первую скобку в сообщене
        
        if symbol == '}':
            flag = 0
            
            # Рандомно выбираем один варинат из скобок
            message_split = msg.split('|')
            msg_select = message_split[randint(0, len(message_split) - 1)]

            # Добавляем выбранные вариант к сообщению
            end_message += msg_select
            msg = ''
            continue

        if flag == 1:
            msg += symbol

        # Рандомизируем символы
        for values in message_randomize.items():
            if symbol in values:
                symbol = values[randint(0, 1)]

        # Собираем сообщение заного
        if flag == 0:
            end_message += symbol

    return end_message


# Получить из файла список пользователей 
def get_users() -> list:
    with open(file='users.txt', mode='r', encoding='UTF-8') as file:
        users_str = file.read()

    users = users_str.strip().split('\n')

    return users