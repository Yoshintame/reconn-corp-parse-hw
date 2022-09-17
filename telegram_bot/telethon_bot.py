import asyncio
from telethon import TelegramClient
from loguru import logger
from aiohttp import web

from config import TELEGRAM_BOT_API_TOKEN, TELEGRAM_API_ID, TELEGRAM_API_HASH
from telegram_bot.bot_handlers import get_bot_events


async def handler(request):
    return  web.Response(text="OK")

# @routes.get('/')
# async def hello(request):
#     return web.Response(text="Hello, world")

async def bot_loop():
    bot = TelegramClient('bot', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await bot.start(bot_token=TELEGRAM_BOT_API_TOKEN)

    events = get_bot_events()
    for key, val in events.items():
        bot.add_event_handler(*val)

    me = await bot.get_me()
    events_keys = "\n".join(events.keys())
    logger.info(f"Bot {me.username} with id {me.id} started with following event handlers: \n{events_keys}")

    await bot.run_until_disconnected()


async def api_server():
    logger.info("here")
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    logger.info("here")
    await runner.setup()
    logger.info("here2")
    site = web.TCPSite(runner, 'localhost', 8080)
    logger.info("here3")
    runn
    await site.start()

    logger.info("======= Serving on http://127.0.0.1:8080/ ======")

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    await asyncio.sleep(100 * 3600)

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def server():
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    web.run_app(app)

async def main():
    await asyncio.wait([
        asyncio.create_task(bot_loop()),
        asyncio.create_task(api_server())
    ])
    #
    # a_server = asyncio.create_task(server())
    # a_bot_loop = asyncio.create_task(bot_loop())
    #
    # await a_server
    # await a_bot_loop


if __name__ == '__main__':

    asyncio.run(main())

