import json

id2handlerInfo = {}


class JSONSerializable:
    def __str__(self):
        return jsonify(self)

    def __repr__(self):
        return jsonify(self, indent=4)


class EventHandlerInfo(JSONSerializable):
    def __init__(self):
        self.selector = None
        self.event = None
        self.uiData = None
        self.handler = None
        self._handler = None
        self.filter_selector = None
        self.stop_propagation = False
        self.throttle = False


def get_handler_info(func) -> EventHandlerInfo:
    function_id = id(func)
    handler_info = id2handlerInfo.get(function_id)
    if handler_info is None:
        handler_info = EventHandlerInfo()
        id2handlerInfo[function_id] = handler_info
    return handler_info


def jsonify(obj, **kwargs) -> str:
    return json.dumps(obj,
                      default=lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith('_')},
                      separators=(',', ':'), **kwargs)


class UIData:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        return self._data[item]

    def __repr__(self):
        return repr(self._data)
