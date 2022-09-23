from aiogram import executor
import asyncio

from parser.parser import corp_authentication
from telegram_bot.bot import dp
from api.api_server import api_server_loop

async def on_startup(x):
    await api_server_loop()


if __name__ == '__main__':
    corp_authentication()
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
