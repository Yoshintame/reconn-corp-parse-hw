from loguru import logger
import asyncio
from aiohttp import web

def say_hello(request):
    return web.Response(
        text="Hello, {}".format(request.match_info['name']))


def four_hundred_one(request):
    return web.HTTPUnauthorized(reason="I must simulate errors.", text="Simulated server error.")


def five_hundred(request):
    return web.HTTPInternalServerError(reason="I must simulate errors.", text="Simulated server error.")


def raise_exception(request):
    raise Exception("Simulated exception")

async def start_site(loop, app, address='localhost', port=8080):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()
    # loop.run_until_complete(site.start())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = web.Application(debug=True)
    app.add_routes([web.get(r'/{name:\d+}', say_hello)])
    app.add_routes([web.get('/401', four_hundred_one)])
    app.add_routes([web.get('/500', five_hundred)])
    app.add_routes([web.get('/exception', raise_exception)])

    loop.create_task(start_site(loop, app))
    loop.run_forever()

