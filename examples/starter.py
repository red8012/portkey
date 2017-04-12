from portkey import *


@onclick('#btn')
async def on_click_btn1(s, d, c):
    s('#btn').text('clicked')

start_app(port=5000)
