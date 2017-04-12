import asyncio
import functools
import logging
import sys
import types

import websockets
# noinspection PyProtectedMember
from werkzeug._reloader import run_with_reloader  # Sorry, I didn't find any easier way to do this.

from .selector import Bundle
from .utilities import *

loop = asyncio.get_event_loop()
clients = set()


def _start_app(log_level, **ws_options):
    logger = logging.getLogger('Portkey')
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
    logger.addHandler(ch)

    async def socket_handler(ws: websockets.WebSocketServerProtocol, path: str):
        try:
            context = types.SimpleNamespace()
            clients.add(ws)
            logger.info('Connection established on %s.', path)
            client_register_info = jsonify({
                'command': 'register',
                'data': list(id2handlerInfo.values())
            })
            # print('handlerInfo', client_register_info)
            await ws.send(client_register_info)
            logger.info('Client events registered.')
            while 1:
                msg = await ws.recv()
                # print('received', msg)
                msg = json.loads(msg)
                handler_id = msg['handler']
                ui_data = UIData(msg['uiData'])
                selector = Bundle(ws)
                # noinspection PyBroadException
                try:
                    # noinspection PyProtectedMember
                    await id2handlerInfo[handler_id]._handler(selector, ui_data, context)
                except:
                    sys.excepthook(*sys.exc_info())
                broadcast = selector.broadcast
                del selector.broadcast
                # print('sending', str(selector))
                await ws.send(str(selector))
                if broadcast.actions:
                    broadcast = str(broadcast)
                    for socket in clients:
                        await socket.send(broadcast)

        except websockets.exceptions.ConnectionClosed:
            logger.info('Connection closed.')
            clients.remove(ws)

    server = websockets.serve(socket_handler, **ws_options)
    loop.run_until_complete(server)
    try:
        logger.info('Server started on ws://%s:%d', ws_options['host'], ws_options['port'])
        loop.run_forever()
    except KeyboardInterrupt:
        pass


def start_app(host='127.0.0.1', port=5000, debug=True, log_level=logging.DEBUG, **ws_options):
    """Start the portkey app running in the event loop. This function should run once and only once for a portkey app. 
    
    Args:
        host: The hostname to listen on. Set this to '0.0.0.0' to have the server available externally
        port: The port of the server
        debug: Whether to automatically reload the program when the code is modified
        log_level: The log level to be passed to Portkey logger
        **ws_options: Other options to be passed to `websockets.serve()`
    """
    starter_function = functools.partial(_start_app, host=host, port=port, log_level=log_level, **ws_options)
    if debug:
        run_with_reloader(starter_function)
    else:
        starter_function()
