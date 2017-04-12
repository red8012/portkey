'use strict';

(function () {
    const PORTKEY_DEBUG = false
    var registeredEvents = []

    function startWebsocket() {
        if ($.portkeyWebsocket == undefined)
            $.portkeyWebsocket = 'ws://127.0.0.1:5000/'
        var socket = new WebSocket($.portkeyWebsocket)
        var queue = []
        var busy = false

        function sendIfNotBusy(message) {
            if (busy) {
                if (PORTKEY_DEBUG) console.log('busy, queued')
                queue.push(message)
            } else {
                if (PORTKEY_DEBUG) console.log('sending', message)
                socket.send(message)
                busy = true
            }
        }

        socket.onmessage = function (event) {
            var message = JSON.parse(event.data)
            var command = message.command
            if (PORTKEY_DEBUG) console.log('received', message)
            if (command == 'register')
                registerEvent(message.data)
            else if (command == 'batch' || command == 'broadcast') {
                const len = message.actions.length
                for (var i = 0; i < len; i++)
                    handleAction(message.actions[i])
                if (queue.length > 0) socket.send(queue.shift())
                else busy = false
            } else if (command == 'immediate') {
                var result = handleAction(message)
                socket.send(JSON.stringify(result))
            } else
                console.error('unhandled command', message)
        }

        socket.onerror = function (event) {
            console.error(event)
        }

        socket.onclose = function (event) {
            console.warn('WebSocket closed. Reconnecting...')
            setTimeout(startWebsocket, 1000)
            const len = registeredEvents.length
            for (var i = 0; i < len; i++) {
                $(registeredEvents[i].selector).off()
            }
            registeredEvents = []
        }

        function makeCallbackFunction(handler) {
            return function (event) {
                if (handler.throttle && busy) return
//                console.log('event', event)
                const attributes = handler.uiData
                const results = Object()

                try {
                    $._target = event.target
                    $._currentTarget = event.currentTarget
                } catch (e) {
                }
                for (var attribute in attributes) {
                    const _a = attributes[attribute]
                    if ($.isArray(_a)) {
                        var selector = _a[1]

                        if (selector == 'target') selector = $._target
                        else if (selector == 'currentTarget') selector = $._currentTarget

                        const returnArray = _a[0]
                        if (returnArray) {
                            const x = $(selector).map(function () {
                                return $(this)[_a[2]](..._a.slice(3))
                            }).get()
                            results[attribute] = x
                        } else {
                            results[attribute] = $(selector)[_a[2]](..._a.slice(3))
                        }
                    } else {
                        results[attribute] = eval(_a)
                    }
                }
                sendIfNotBusy(JSON.stringify({
                    handler: handler.handler,
                    uiData: results
                }))
                if (handler.stop_propagation) {
                    event.stopPropagation()
                }
            }

        }

        function registerEvent(data) {
            registeredEvents.push.apply(registeredEvents, data)

            const len = data.length
            for (var i = 0; i < len; i++) {
                const handler = data[i]
                $(handler.selector).on(handler.event, handler.filter_selector,
                    makeCallbackFunction(handler))
            }
            if (PORTKEY_DEBUG) console.log('registeredEvents', registeredEvents)

            $('body').trigger('_Portkey:ready').off('_Portkey:ready')
        }

        function handleAction(action) {
//            console.log('action', action)
            var result
            if (action.type == 'selector') {
                var selector
                if (action.selector == 'target') selector = $($._target)
                else if (action.selector == 'currentTarget') selector = $($._currentTarget)
                else selector = $(action.selector)
                const subActions = action.sub_actions
                const len = subActions.length
                for (var i = 0; i < len; i++) {
                    const subAction = subActions[i]
                    const len = subAction.length
                    for (var j = 1; j < len; j++) {
                        if (Number.isInteger(subAction[j].handler)) {
                            subAction[j] = makeCallbackFunction(
                                $.extend(true, {}, subAction[j])
                            )
                        }
                    }
                    selector = selector[subAction[0]](...subAction.slice(1))
                }
                result = selector
            } else if (action.type == 'eval') {
                const code = action.code
                const data = action.data
                for (var k in data)
                    window[k] = data[k]
                result = eval(code)
            } else console.error('unhandled action')
            return result
        }
    }
    $(document).ready(startWebsocket)
})()
