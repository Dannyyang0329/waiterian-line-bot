import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from utils import *


app = Flask(__name__)
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', default=''))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


arr = []

@handler.add(MessageEvent)
def handle_message(event):
    arr.append('a')
    print(arr)

    token = event.reply_token
    msg = event.message.text if event.message.type == 'text' else ''

    cur_state = get_state(event)

    # idle state
    if cur_state == 'idle':
        if msg == 'WAITERIAN':
            show_carousel_images(event)     # idle -> idle

        if msg == 'FOOD':
            show_search_filter(event)       # idle -> search_filter

    # search_filter state
    if cur_state == 'search_filter':
        if msg == '設定位置訊息':
            show_location_message(event)    # search_filter -> get_location
        if msg == '設定搜索半徑':
            show_radius_message(event)      # search_filter -> get_radius
        if msg == '設定價錢標準':
            show_price_message(event)       # search_filter -> get_price
        if msg == '使用關鍵字搜尋':
            show_keyword_message(event)     # search_filter -> get_keyword
        if msg == '顯示所有設定':
            show_all_setting(event)         # search_filter -> search_filter
        if msg == '開始搜尋':
            show_all_restaurant(event)

    # get_location state
    if cur_state == 'get_location':
        get_the_location(event)             # get_location -> search_filter

    # get_radius state
    if cur_state == 'get_radius':
        get_the_radius(event)               # get_radius -> search-filter

    # get_price state
    if cur_state == 'get_price':
        get_the_price(event)                # get_price -> search-filter

    # get_keyword state
    if cur_state == 'get_keyword':
        get_the_keyword(event)              # get_keyword -> search-filter


    if msg == 'ROULETTE':
        line_bot_api.reply_message(token, TextSendMessage(text='I get ROULETTE'))
    if msg == 'INFORMATION':
        info = f"""
            Type: {event.source.type}
            State:{cur_state}
        """
        line_bot_api.reply_message(token, TextSendMessage(text=info))


if __name__ == "__main__":
    load_dotenv()
    app.run()
