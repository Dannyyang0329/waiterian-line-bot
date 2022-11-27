import os
import random
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, LocationAction, MessageAction
)

from flex_message import (
    get_carousel_images_json, get_single_restaurant_json, get_search_filter_json
)

from database_control import (
    insert_data, select_data, find_data, update_state, delete_data
)

from restaurant_query import (
    get_restaurant, get_restaurant_photo, get_restaurant_url
)


app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', default=''))
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


def get_id(event):
    if event.source.type == 'user':
        return event.source.user_id
    if event.source.type == 'group':
        return event.source.group_id


def get_state(event):
    if event.source.type == 'user':
        data = find_data(event.source.user_id)
        if len(data) == 0:
            new_data = ('user', event.source.user_id, 'idle')
            insert_data(new_data)
            return 'idle'
        else:
            return data[0][3]
    if event.source.type == 'group':
        data = find_data(event.source.group_id)
        if len(data) == 0:
            new_data = ('group', event.source.group_id, 'idle')
            insert_data(new_data)
            return 'idle'
        else:
            return data[0][3]


def show_carousel_images(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_carousel_images_json()
        )
    )

def show_search_filter(event):
    update_state(get_id(event), 'state', 'search_filter')
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'search filter',
            contents = get_search_filter_json()
        )
    )

def show_location_message(event):
    update_state(get_id(event), 'state', 'get_location')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送位置訊息了喔~",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=LocationAction(label="傳送位置")
                    )
                ]
            )
        )
    )


def show_radius_message(event):
    update_state(get_id(event), 'state', 'get_radius')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送搜索半徑了喔~",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="500m",text=">> 500")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="1000m",text=">> 1000")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="1500m",text=">> 1500")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="2000m",text=">> 2000")
                    ),
                ]
            )
        )
    )


def show_price_message(event):
    update_state(get_id(event), 'state', 'get_price')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送價錢標準了喔~",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="LV 0",text=">> 0")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="LV 1",text=">> 1")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="LV 2",text=">> 2")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="LV 3",text=">> 3")
                    ),
                ]
            )
        )
    )


def show_keyword_message(event):
    update_state(get_id(event), 'state', 'get_keyword')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送關鍵字了喔~",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="日式",text=">> 日式")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="美式",text=">> 美式")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="台式",text=">> 台式")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="泰式",text=">> 泰式")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="韓式",text=">> 韓式")
                    ),
                ]
            )
        )
    )


def show_all_setting(event):
    data = find_data(get_id(event))[0]
    radius = 3000 if data[6] is None else data[6]
    price_LV = 0 if data[7] is None else data[7]
    keyword = '' if data[8] is None else data[8]

    setting_str  = f"Lat :        {data[4]}\n"
    setting_str += f"Lng :        {data[5]}\n"
    setting_str += f"Radius :     {radius}\n"
    setting_str += f"Price LV :   {price_LV}\n"
    setting_str += f"Keyword :    {keyword}\n"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=setting_str)
    )


@handler.add(MessageEvent)#, message=TextMessage)
def handle_message(event):
    msg = ''
    if event.message.type == 'text':
        msg = event.message.text

    token = event.reply_token

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
            update_state(get_id(event), 'state', 'idle')
            line_bot_api.reply_message(token, TextSendMessage(text='Searching'))
            data = find_data(get_id(event))[0]
            response = get_restaurant (
                data[4], data[5], data[6], data[7], data[8]
            )
            response = response[(random.randrange(0, len(response)))]
            
            line_bot_api.reply_message(
                token, 
                FlexSendMessage(
                    alt_text = "RESTAURANT", 
                    contents = get_single_restaurant_json (
                        get_restaurant_photo(response),
                        response['name'],
                        response['rating'],
                        response['price_level'],
                        response['vicinity'],
                        get_restaurant_url(response)
                    )
                )
            )


    # get_location state
    if cur_state == 'get_location':
        print(event)
        if event.message.type == 'location':
            update_state(get_id(event), 'lat', event.message.latitude)
            update_state(get_id(event), 'lng', event.message.longitude)
            update_state(get_id(event), 'state', 'search_filter')
            line_bot_api.reply_message(token, TextSendMessage(text='設定位置訊息成功!'))

    # get_radius state
    if cur_state == 'get_radius':
        if event.message.type == 'text':
            tmp = msg.split(" ")
            if len(tmp) > 1 and tmp[0] == '>>':
                update_state(get_id(event), 'radius', int(tmp[1]))
                update_state(get_id(event), 'state', 'search_filter')
                line_bot_api.reply_message(token, TextSendMessage(text='設定搜索半徑成功!'))

    # get_price state
    if cur_state == 'get_price':
        if event.message.type == 'text':
            tmp = msg.split(" ")
            if len(tmp) > 1 and tmp[0] == '>>':
                update_state(get_id(event), 'min_p', int(tmp[1]))
                update_state(get_id(event), 'state', 'search_filter')
                line_bot_api.reply_message(token, TextSendMessage(text='設定價錢標準成功!'))

    # get_keyword state
    if cur_state == 'get_keyword':
        if event.message.type == 'text':
            tmp = msg.split(" ")
            if len(tmp) > 1 and tmp[0] == '>>':
                update_state(get_id(event), 'key_w', tmp[1])
                update_state(get_id(event), 'state', 'search_filter')
                line_bot_api.reply_message(token, TextSendMessage(text='設定關鍵字成功!'))


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
