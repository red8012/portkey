import inspect

from .utilities import *


def on(selector: str, event: str, filter_selector: str=None, throttle=False, stop_propagation=False):
    """Register a coroutine function as a handler for the given event.
    Corresponding to `$(selector).on(event, filter_selector, ...)` in jQuery

    Args:
        selector: A jQuery selector expression
        event: One or more space-separated event types and optional namespaces, such as "click".
        filter_selector: a selector string to filter the descendants of the selected elements that trigger the event.
            If this argument is omitted, the event is always triggered when it reaches the selected element.
        throttle: Whether to discard events when Portkey is busy.
            Should set to true if the event is going to fire at very high frequency.
            If set to false, all events will be queued and handled.
        stop_propagation: Prevents the event from bubbling up the DOM tree, 
            preventing any parent handlers from being notified of the event.

    Returns: A decorator that returns the original function.

    """

    def decorator(func):
        assert inspect.iscoroutinefunction(func), \
            'Only a coroutine function (a function defined with an async def syntax)' \
            ' can be registered as an event handler.'
        handler_info = get_handler_info(func)
        # assert handler_info.handler is None, \
        #     'You should only register one event on a handler function.'
        handler_info._handler = func
        handler_info.handler = id(func)
        handler_info.selector = selector
        handler_info.event = event
        handler_info.filter_selector = filter_selector
        handler_info.throttle = throttle
        handler_info.stop_propagation = stop_propagation
        return func
    return decorator


def onclick(selector: str, filter_selector: str=None, throttle=False, stop_propagation=False):
    """A shorthand for `on(selector, 'click').

    Args:
        selector: a jQuery selector expression
        filter_selector: a selector string to filter the descendants of the selected elements that trigger the event.
            If this argument is omitted, the event is always triggered when it reaches the selected element.
        throttle: Whether to discard events when Portkey is busy.
            Should set to true if the event is going to fire at very high frequency.
            If set to false, all events will be queued and handled.
        stop_propagation: Prevents the event from bubbling up the DOM tree, 
            preventing any parent handlers from being notified of the event.

    Returns: A decorator that returns the original function.

    """
    return on(selector, 'click',
              filter_selector=filter_selector, throttle=throttle, stop_propagation=stop_propagation)


def ready():
    """Register a coroutine function to be triggered when the Portkey client is ready.

    Returns: A decorator that returns the original function.

    """
    return on('body', '_Portkey:ready')


def _make_ui_data_tuple(v):
    if isinstance(v, tuple):
        return (False,) + v
    if isinstance(v, list):
        return [True] + v
    if isinstance(v, str):
        return v
    raise AttributeError('The value must be a tuple, a list or a string.')


def with_ui_data(**d):
    """Specifies the attributes to be retrieved from the Portkey client. 

    Args:
        **d: Key: variable name; value: attribute(s) to get 
            If the value is a string, it will be evaluated directly in the client.
            If the value is a tuple, it will be evaluated as `$(first).second(third, ...)`.
            If the value is a list, it works similarly as the tuple case, but returns the attributes of 
            EVERY matched element as a list.
            For the tuple and list cases, if the first element is 'target' or 'currentTarget', it will be evaluated as
            `$(event.target)` or `$(event.currentTarget)` respectively.
            
    Returns: A decorator that returns the original function.

    """

    def decorator(func):
        handler_info = get_handler_info(func)
        assert handler_info.uiData is None, \
            'You should only register a set of remote attributes on a handler function.'
        handler_info.uiData = {k: _make_ui_data_tuple(v) for k, v in d.items()}
        return func
    return decorator
