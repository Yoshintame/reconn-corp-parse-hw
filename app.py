from aiogram import executor

from parser.parser import corp_authentication
from telegram_bot.bot import dp

if __name__ == '__main__':
    corp_authentication()
    executor.start_polling(dp, skip_updates=True)
