from portkey import *
import asyncio


@onclick('#btn')
async def on_click_btn1(s, d, c):
    s('#btn').text('clicked')


@onclick('#simple-button')
async def simple_button_handler(s, d, c):
    s('#simple-button').text('clicked!').toggleClass('uk-button-primary')


@on('#hello-name', 'keyup change')
@with_ui_data(name=('#hello-name', 'val'))
async def say_hello(s, d, c):
    s('#hello-message').text('Hello ' + d.name)


@ready()
async def on_ready(s, d, c):
    c.counter = 0
    s('#connection-alert').addClass('uk-hidden')


@onclick('#add-one')
async def counter_add_one(s, d, c):
    c.counter += 1
    s('#counter').text(c.counter)


@on('.input-number', 'change keyup')
@with_ui_data(numbers=['.input-number', 'val'])
async def calculate_addition(s, d, c):
    s('#adder-result').text(sum(int(i) for i in d.numbers))


@onclick('.btn-target')
@with_ui_data(who=('currentTarget', 'text'))
async def on_click_target(s, d, c):
    s('#target-message').text(d.who + ' was clicked')
    s('currentTarget').toggleClass('uk-button-primary')


@onclick('#alert')
@with_ui_data(pi='document.getElementById("just-a-div").textContent')
async def on_click_alert(s, d, c):
    s.eval('alert(myObject.pi)', myObject={'pi': d.pi})


@onclick('#btn-animate')
async def on_click_animate(s, d, c):
    s('#yo-message').animate({'opacity': 0}, 1000, animate_part2)

async def animate_part2(s, d, c):
    s('#yo-message').animate({'opacity': 1}, 1000)


broadcast_count = 0


@onclick('#broadcast-add-one')
async def on_click_broadcast(s, d, c):
    global broadcast_count
    broadcast_count += 1
    s.broadcast('#broadcasted-counter').text(broadcast_count)


@with_ui_data(selected=('input[name=radio]:checked', 'val'))
@onclick('#get-value')
async def on_click_get_value(s, d, c):
    value = await s.immediate('#input-' + d.selected).val()
    await s.eval_immediately(
        'document.getElementById("selected-value").textContent = "Got " + value',
        value=d.selected + ' = ' + value
    )


@onclick('#add-button')
async def on_click_add_button(s, d, c):
    btn = '<button class="uk-button uk-button-secondary"> click me </button>'
    s('#button-area').append(btn)


@onclick('#button-area', filter_selector='button')
async def on_click_dynamic_buttons(s, d, c):
    s('target').toggleClass('uk-button-danger')


async def run_progress(s):
    await s.immediate('#progress').val(0)
    await asyncio.sleep(0.3)
    for i in range(0, 101, 10):
        await asyncio.sleep(0.1)
        await s.immediate('#progress').val(i)


@onclick('#btn-without-throttle')
async def on_click_without_throttle(s, d, c):
    await run_progress(s)


@onclick('#btn-with-throttle', throttle=True)
async def on_click_with_throttle(s, d, c):
    await run_progress(s)


start_app(debug=True, host='0.0.0.0', port=5002)
