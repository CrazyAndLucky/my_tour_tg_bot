import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from data import DatabaseManager



load_dotenv('.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
db = DatabaseManager('data/database.db')


admins = []
users = []


class UsersManager:
    async def add_new_user(self, id, username, first_name, last_name):

        await db.query('INSERT OR REPLACE INTO all_users VALUES (?, ?, ?, ?)', (id, username, first_name, last_name))


um = UsersManager()