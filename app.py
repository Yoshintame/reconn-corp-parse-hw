import asyncio
import requests
from flask_restful import Api, Resource
from flask import Flask

from parser.parser import corp_authentication, headers
from config import TELEGRAM_BOT_API_TOKEN, TELEGRAM_API_ID, TELEGRAM_API_HASH
from telegram_bot.telethon_bot import bot_loop
from api.api_server import PublicApi


app = Flask(__name__)
api = Api(app)
api.add_resource(PublicApi, "/api/hw<int:hw_number>")


async def main():
    await asyncio.wait([
        asyncio.create_task(bot_loop()),
    ])

if __name__ == '__main__':
    corp_session = requests.Session()
    corp_authentication(corp_session, headers)

    app.run(debug=True)

    bot = TelegramClient('bot', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    asyncio.run(main())