from sqlite3 import connect

class DB_Manager:
    def __init__(self, path):
        self.connect = connect(path)
        self.connect.execute('pragma foreign_keys = on')
        self.connect.commit()

        # Создаем курсор
        self.cursor = self.connect.cursor()

    
    # Функция для обращения к базе, достать или извлечь данные
    def query(self, arg, values=None):
        if values is not None:
            self.cursor.execute(arg, values)
        else:
            self.cursor.execute(arg)

        # Записываем изменения в базу
        self.connect.commit()

    
    def create_tables(self):
        self.query(
            'CREATE TABLE IF NOT EXISTS accounts (unique_id text PRIMARY KEY, path_to_tdata text, proxy text, status text, time DATETIME, proxy_type TEXT, messages INT, spam_messages INT, step INT, phone TEXT)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS blacklist (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS chanels (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS chats (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS bots (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS phones (phones text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS bio (bio text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS mes_in_chat (usr_id text PRIMARY KEY, mes_id INT)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS config (dual_message INT DEFAULT 0, count_send_msg INT DEFAULT 0, spam_delay TEXT DEFAULT "10 30")'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS spam_users (username text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS proxy (proxy text PRIMARY KEY)'
        )
        self.query(
            'CREATE TABLE IF NOT EXISTS links (id INTEGER, link TEXT, msg_id INT, count_msg INT, PRIMARY KEY (id AUTOINCREMENT))'
        )
        
        



    def fetchall(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)

        return self.cursor.fetchall()
    

    def fetchone(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)

        return self.cursor.fetchone()
    

    def __del__(self):
        self.connect.close()
            
