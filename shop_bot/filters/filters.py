from aiogram import filters
from aiogram.types import Message

from loader import db, admins, users


class IsAdmin(filters.Filter):
     async def __call__(self, message: Message):
          # admins = []
          
          # data = await db.fetchall('SELECT * FROM admins')
          # for value in data:
          #      admins.append(value[0])

          return message.from_user.id in admins
     

class IsUser(filters.Filter):
     async def __call__(self, message: Message):
          # admins = []
          
          # data = await db.fetchall('SELECT * FROM admins')
          # for value in data:
          #      admins.append(value[0])

          return message.from_user.id in users