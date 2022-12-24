import os
import random
from dotenv import load_dotenv

from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from flex_message import *
from search_recipe import *
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


def show_information(event, state):
    msg = event.message.text.upper() if event.message.type == 'text' else ''
    if msg == 'INFORMATION':
        info = "您現在的狀態是"
        if state == 'idle':
            info += 'idle'
        elif state == 'search_restaurant':
            info += 'search_restaurant'
        elif state == 'get_location':
            info += 'get_location'
        elif state == 'get_radius':
            info += 'get_radius'
        elif state == 'get_price_level':
            info += 'get_price_level'
        elif state == 'get_keyword':
            info += 'get_keyword'
        elif state == 'search_recipe':
            info += 'search_recipe'
        elif state == 'dessert_recipe':
            info += 'dessert_recipe'
        elif state == 'dish_recipe':
            info += 'dish_recipe'
        elif state == 'exotic_recipe':
            info += 'exotic_recipe'
        elif state == 'drink_recipe':
            info += 'drink_recipe'
        elif state == 'wait_target_recipe':
            info += 'wait_target_recipe'
        elif state == 'help':
            info += 'help'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))


def show_mainmenu(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_mainmenu_json()
        )
    )


def show_FSM(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url='https://i.imgur.com/GsRHP8v.png',
            preview_image_url='https://i.imgur.com/GsRHP8v.png'
        )
    )


def show_search_filter(event):
    # update_state(get_id(event), 'state', 'search_filter')
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'search filter',
            contents = get_search_restaurant_json()
        )
    )


def show_location_message(event):
    # update_state(get_id(event), 'state', 'get_location')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送位置訊息了喔!",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=LocationAction(label="傳送位置"))
                ]
            )
        )
    )


def show_radius_message(event):
    # update_state(get_id(event), 'state', 'get_radius')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送搜索半徑了喔!",
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


def show_price_level_message(event):
    # update_state(get_id(event), 'state', 'get_price')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送價錢標準了喔!",
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
    # update_state(get_id(event), 'state', 'get_keyword')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="可以傳送關鍵字了喔!",
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

    setting_str  = f"Latitude    : {latitude}\n"
    setting_str += f"Longtitude  : {longtitude}\n"
    setting_str += f"Radius      : {radius}\n"
    setting_str += f"Price Level : {price_LV}\n"
    setting_str += f"Keyword     : {keyword}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=setting_str)
    )


def show_all_restaurant(event):
    # update_state(get_id(event), 'state', 'idle')
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
    restaurant_index = random.sample(list(range(restaurant_num)), restaurant_num)

    for i in restaurant_index:
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


def print_quit_msg(event, state):
    if state == 'search_restaurant':
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text='結束餐廳搜尋!')
        )
    elif state == 'search_recipe':
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text='結束菜譜搜尋!')
        )
    elif state == 'help':
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text='結束幫助!')
        )


def get_the_location(event):
    if event.message.type == 'location':
        update_state(get_id(event), 'lat', event.message.latitude)
        update_state(get_id(event), 'lng', event.message.longitude)
        # update_state(get_id(event), 'state', 'search_filter')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定位置訊息成功!'))
        return True
    return False


def get_the_radius(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'radius', int(tmp[1]))
            # update_state(get_id(event), 'state', 'search_filter')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定搜索半徑成功!'))
            return True
    return False


def get_the_price_level(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'min_p', int(tmp[1]))
            # update_state(get_id(event), 'state', 'search_filter')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定價錢標準成功!'))
            return True
    return False


def get_the_keyword(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'key_w', tmp[1])
            # update_state(get_id(event), 'state', 'search_filter')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定關鍵字成功!'))
            return True
    return False


def show_search_recipe(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'search recipe',
            contents = get_search_recipe_json()
        )
    )


def show_dessert_recipe_category(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_dessert_recipe_json()
        )
    )


def show_dish_recipe_category(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_dish_recipe_json()
        )
    )


def show_drink_recipe_category(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_drink_recipe_json()
        )
    )


def show_exotic_recipe_category(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'carousel images',
            contents = get_exotic_recipe_json()
        )
    )


def get_the_target_recipe(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            show_all_recipe(event, 'wait_target_recipe', tmp[1])
            return True
    return False


def show_all_recipe(event, type, category):
    selected_recipes = []
    if type == 'wait_target_recipe':
        selected_recipes = get_search_recipe(category)
    else:
        selected_recipes = get_recipe(type, category)
   
    if len(selected_recipes) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有符合的食譜")
        )
        return

    recipe_list = []
    for recipe in selected_recipes:
        try:
            restaurant = get_single_recipe_json(
                recipe['img_url'],
                recipe['name'],
                recipe['ingredient'],
                recipe['href']
            )
            recipe_list.append(restaurant)
        except Exception as e:
            print(e)

    line_bot_api.reply_message(
        event.reply_token, 
        FlexSendMessage(
            alt_text = "RESTAURANTS", 
            contents =  {
                "type": "carousel",
                "contents": recipe_list
            }
        )
    )


def show_help_manual_category(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text = 'help_manual_category',
            contents = get_help_manual_category_json()
        )
    )

def show_help_manual(event, type):
    if type == 'search_restaurant':
        text  = '幫助: 搜尋餐廳\n'
        text += ' Step1 : 點選RESTAURANT的icon開始準備搜尋餐廳\n'
        text += ' Step2 : 根據下列的篩選器選擇您要搜尋的範圍\n'
        text += '  • 位置訊息(必選)\n'
        text += '  • 搜索半徑(可選)\n'
        text += '  • 價錢標準[0-3](可選)\n'
        text += '  • 關鍵字搜尋(可選)\n'
        text += ' Step3 : 點選"顯示所有設定"確認設定正確\n'
        text += ' Step4 : 點選"開始搜尋"即可尋找出附近的餐廳\n'
        text += ' Step4 : 點選"離開"回到主選單\n'
        text += '提醒: 篩選器的搜尋需要用">> "來作為前綴\n'
        text += '  • e.g. >> 鍋燒意麵'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif type == 'search_recipe':
        text  = '幫助: 搜尋食譜\n'
        text += ' Step1 : 點選RECIPE的icon開始準備搜尋食譜\n'
        text += ' Step2 : 選擇您想要的食譜類型或是特定菜餚的名字\n'
        text += '  • 點心與甜點\n'
        text += '  • 家常料理\n'
        text += '  • 異國料理\n'
        text += '  • 冰品與飲品\n'
        text += ' Step3 : 選擇更詳細的分類\n'
        text += ' Step4 : 點選"QUIT"回到主選單\n'
        text += '提醒: 輸入特定菜姚名稱時需要用">> "來作為前綴\n'
        text += '  • e.g. >> 壽司'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
