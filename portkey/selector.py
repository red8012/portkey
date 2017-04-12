from .decorators import *
import json
import inspect
import websockets

try:
    # noinspection PyPackageRequirements
    from dominate.tags import html_tag
except ImportError:
    # noinspection PyPep8Naming
    class html_tag:
        pass


def preprocess_jquery_arguments(x):
    if isinstance(x, html_tag):
        return str(x)
    if inspect.iscoroutinefunction(x):
        on(None, None)(x)
        return id2handlerInfo[id(x)]
    return x


class Selector(JSONSerializable):
    def __init__(self, selector: str, websocket: websockets.WebSocketServerProtocol=None):
        self.selector = selector
        self.sub_actions = []
        self.type = 'selector'
        self._websocket = websocket
        if websocket is not None:
            self.command = 'immediate'

    def __getattr__(self, action):
        if self._websocket is None:
            def func(*args):
                args = tuple(preprocess_jquery_arguments(a) for a in args)
                self.sub_actions.append((action,) + args)
                return self
            return func

        async def func(*args):
            self.sub_actions.append((action,) + args)
            await self._websocket.send(str(self))
            return json.loads(await self._websocket.recv())
        return func


class Bundle(JSONSerializable):
    def __init__(self, websocket: websockets.WebSocketServerProtocol, command='batch'):
        self.command = command
        self.actions = []
        self._websocket = websocket
        if command == 'batch':
            self.broadcast = Bundle(websocket, command='broadcast')

    def __call__(self, selector: str):
        s = Selector(selector)
        self.actions.append(s)
        return s

    def eval(self, code: str, **data):
        """Run arbitrary code in the browser after the handler returns. 
        Meant to be used for interacting with 3rd-party Javascript libraries or things not provided by jQuery API.

        Args:
            code: The Javascript code to be evaluated in the browser
            **data: The data supplied to be used by the Javascript code, must be JSON serializable
                All data will be attached to the `window` object.
        """
        self.actions.append({'type': 'eval', 'code': code, 'data': data})

    async def eval_immediately(self, code: str, **data):
        """Run arbitrary code in the browser and get the evaluated result back immediately.
        Must be awaited.

        Args:
            code: The Javascript code to be evaluated in the browser
            **data: The data supplied to be used by the Javascript code, must be JSON serializable
                All data will be attached to the `window` object.

        Returns: The evaluated result from browser

        """
        await self._websocket.send(json.dumps({
            'command': 'immediate',
            'type': 'eval',
            'code': code,
            'data': data
        }))
        return json.loads(await self._websocket.recv())

    def immediate(self, selector: str) -> Selector:
        """Execute jQuery function and get the result back immediately.
        Must be awaited.
        Meant to be used for dynamically getting attributes from UI.

        Args:
            selector: A jQuery selector expression

        Returns: The resulting selector object

        """
        return Selector(selector, websocket=self._websocket)
