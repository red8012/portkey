from portkey import *


@onclick('#btn')
async def on_click_btn1(s, d, c):
    s('#btn').text('clicked')

start_app(host='0.0.0.0', port=5000)
