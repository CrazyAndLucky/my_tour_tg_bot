# from sqlite3 import connect 
from aiosqlite import connect 

class DatabaseManager: 

    def __init__(self, path):
        self.path = path
        
        
    async def connect(self):
        self.conn = await connect(self.path)
        await self.conn.execute('pragma foreign_keys = on')
        await self.conn.commit()
        self.cur = await self.conn.cursor()

    async def query(self, arg, values=None):
        if values is None:
            await self.cur.execute(arg)
        else:
            await self.cur.execute(arg, values)
        await self.conn.commit()

    async def create_tables(self):
        await self.query(
            'CREATE TABLE IF NOT EXISTS all_users (id INTEGER PRIMARY KEY, username TEXT, '
            'first_name TEXT, last_name TEXT)')
        

        await self.query(
            'CREATE TABLE IF NOT EXISTS products (idx text, title text, '
            'body text, photo blob, price int, download_link text)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS orders (cid int, idx text, '
            'title text, body text, photo blob, ptice int, download_link)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS completed_orders (cid int, idx text, '
            'title text, body text, photo blob, ptice int)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS cart (cid int, idx text, '
            'quantity int)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS categories (idx text, title text)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS wallet (cid int, blance real)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS questions (cid int, question text)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS users (cid int UNIQUE, status int)')
        await self.query(
            'CREATE TABLE IF NOT EXISTS admins (cid int UNIQUE)')
        

    async def fetchone(self, arg, values=None):
        if values is None:
            await self.cur.execute(arg)
        else:
            await self.cur.execute(arg, values)

        return await self.cur.fetchone()
    

    async def fetchall(self, arg, values=None):
        if values is None:
            await self.cur.execute(arg)
        else:
            await self.cur.execute(arg, values)

        return await self.cur.fetchall()
    

    async def close(self):
        await self.conn.close()

