from aiogram import Bot, Dispatcher
from data.storage import DatabaseManager

from WalletPay import AsyncWalletPayAPI, WebhookManager

from data import config

wp = AsyncWalletPayAPI(api_key=config.WALLET_API)
wm = WebhookManager(client=wp)