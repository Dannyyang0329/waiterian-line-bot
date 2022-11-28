import os
from dotenv import load_dotenv

from linebot import LineBotApi
from linebot.exceptions import 
from linebot.models import *

from flex_message import *
from database_control import *
from restaurant_query import *


line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', default=''))


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
                    QuickReplyButton(action=LocationAction(label="傳送位置"))
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
                    QuickReplyButton(action=MessageAction(label="500m",text=">> 500")),
                    QuickReplyButton(action=MessageAction(label="1000m",text=">> 1000")),
                    QuickReplyButton(action=MessageAction(label="1500m",text=">> 1500")),
                    QuickReplyButton(action=MessageAction(label="2000m",text=">> 2000"))
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
                    QuickReplyButton(action=MessageAction(label="LV 0",text=">> 0")),
                    QuickReplyButton(action=MessageAction(label="LV 1",text=">> 1")),
                    QuickReplyButton(action=MessageAction(label="LV 2",text=">> 2")),
                    QuickReplyButton(action=MessageAction(label="LV 3",text=">> 3"))
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
                    QuickReplyButton(action=MessageAction(label="無",text=">> 無")),
                    QuickReplyButton(action=MessageAction(label="日式",text=">> 日式")),
                    QuickReplyButton(action=MessageAction(label="美式",text=">> 美式")),
                    QuickReplyButton(action=MessageAction(label="台式",text=">> 台式")),
                    QuickReplyButton(action=MessageAction(label="泰式",text=">> 泰式")),
                    QuickReplyButton(action=MessageAction(label="韓式",text=">> 韓式"))
                ]
            )
        )
    )


def show_all_setting(event):
    data = find_data(get_id(event))
    if len(data) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Data not found")
        )
        return

    data = data[0]

    latitude    = 'None' if data[4] is None else data[4]
    longtitude  = 'None' if data[5] is None else data[5]
    radius      =  3000  if data[6] is None else data[6]
    price_LV    =     0  if data[7] is None else data[7]
    keyword     =     '' if data[8] is None else data[8]

    setting_str  = f"Lat :        {latitude}\n"
    setting_str += f"Lng :        {longtitude}\n"
    setting_str += f"Radius :     {radius}\n"
    setting_str += f"Price LV :   {price_LV}\n"
    setting_str += f"Keyword :    {keyword}\n"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=setting_str)
    )


def show_all_restaurant(event):
    update_state(get_id(event), 'state', 'idle')
    datas = find_data(get_id(event))
   
    if len(datas) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="資料庫錯誤")
        )
        return

    data = datas[0]
    responses = get_restaurant(
        data[4], data[5], data[6], data[7], data[8]
    )
    if responses == 'ERROR':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="搜尋錯誤")
        )
        return
    if len(responses) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有符合的商家")
        )
        return

    restaurants = []
    restaurant_num = 10 if len(responses)>10 else len(responses)

    for i in range(restaurant_num):
        try:
            restaurant = get_single_restaurant_json(
                get_restaurant_photo(responses[i]),
                responses[i]['name'],
                responses[i]['rating'],
                responses[i]['price_level'],
                responses[i]['vicinity'],
                get_restaurant_url(responses[i])
            )
            restaurants.append(restaurant)
        except Exception as e:
            print(e)

    line_bot_api.reply_message(
        event.reply_token, 
        FlexSendMessage(
            alt_text = "RESTAURANTS", 
            contents =  {
                "type": "carousel",
                "contents": restaurants
            }
        )
    )
