from portkey import *
from time import time

try:
    import uvloop
    import asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print('warning: not using uvloop')


@onclick('#start')
async def ping(s, d, c):
    c.counter = 0
    c.start = time()
    s('body').trigger('e')


@on('body', 'e')
async def pong(s, d, c):
    if c.counter >= 100:
        s('#result').text((time() - c.start) * 10)
        return
    c.counter += 1
    s('body').trigger('e')


start_app(host='0.0.0.0', port=5001)
