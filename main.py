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
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, LocationAction
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
                        action=LocationAction(label=">> 500")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 1000")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 1500")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 2000")
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
                        action=LocationAction(label=">> 0")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 1")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 2")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 3")
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
                        action=LocationAction(label=">> 日式")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 美式")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 台式")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 泰式")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label=">> 韓式")
                    ),
                ]
            )
        )
    )


def show_all_setting(event):
    data = find_data(get_id(event))
    setting_str = f"Lat :        {data[4]}\n"
    setting_str += f"Lng :        {data[5]}\n"
    setting_str += f"Min price :  {data[6]}\n"
    setting_str += f"Keyword :    {data[7]}\n"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=setting_str)
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
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



        # line_bot_api.reply_message(token, TextSendMessage(text='I get FOOD'))
        # response = get_restaurant (
        #     22.993,
        #     120.219,
        #     1000,
        # )
        # response = response[(random.randrange(0, len(response)))]
        #
        # line_bot_api.reply_message(
        #     token, 
        #     FlexSendMessage(
        #         alt_text = "RESTAURANT", 
        #         contents = get_single_restaurant_json (
        #             get_restaurant_photo(response),
        #             response['name'],
        #             response['rating'],
        #             response['price_level'],
        #             response['vicinity'],
        #             get_restaurant_url(response)
        #         )
        #     )
        # )
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
