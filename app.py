import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time

from datetime import datetime

from aiohttp import web

def index(request):
    name = request.match_info.get('name', 'World')
    text = '<h1>Hello, {0} !</h1>'.format(name)
    return web.Response(body=text)


async def init(loop):
    app = web.Application(loop=loop)

    app.router.add_get('/', index)
    app.router.add_get('/{name}', index)

    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8003)

    logging.info('server started at http://127.0.0.1:8003....')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

