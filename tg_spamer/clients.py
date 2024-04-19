import asyncio
from tg_spamer.loader import Config, Links, Accounts, db
from tg_spamer.tools import get_clients, mon_patching


mon_patching()

loop = asyncio.get_event_loop()
clients_list = loop.run_until_complete(get_clients())

config = Config()
links_manager = Links()
accounts_manager = Accounts()



async def update_clients_list(distribute_proxies: bool = False):
    global clients_list
    clients_list.clear()
    clients_list_update = await get_clients(distribute_proxies=distribute_proxies)
    clients_list.update(clients_list_update) 