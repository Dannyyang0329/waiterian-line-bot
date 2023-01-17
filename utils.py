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
        info = ""
        if state == 'idle':
            info += """
您現在的狀態是:idle
您可以使用以下的操作:
1. SEARCH RESTAURANT
根據您等等設定的條件，搜尋特定區域的餐廳。
2. SEARCH RECIPE
根據您等等設定的條件，搜尋食譜。
3. INFORMATION
顯示幫助訊息，幫助您更快了解如何使用機器人!
            """
        elif state == 'search_restaurant':
            info += """
您現在的狀態是:search_restaurant
您需要設定條件，幫助機器人尋找附近的餐廳
* 只有正在營業的餐廳會顯示
* 隱藏美食機器人尚未有辦法搜尋到
* 各項設定會保留您上次搜尋的設定
* 若是想要退出現在的狀態，請點選離開，或輸入QUIT

您可以使用以下的操作:
1. 位置訊息 (SET LOCATION)
使用line的位置訊息功能，提供您想搜尋的地點
2. 搜索半徑 (SET RADIUS)
根據您設定的地點，設定搜索半徑(公尺為單位)
(注意: 設定需以">> "作為前綴符號)
(例如: >> 1000)
3. 價錢標準 (SET PRICE LEVEL)
設定價錢標準(google map的標準)
(注意: 請輸入">> 0~3"進行設定)
(例如: >> 1)
4. 關鍵字搜尋 (SET KEYWORD)
使用關鍵字進行搜尋
(注意: 設定需以">> "作為前綴符號)
(例如: >> 鍋燒意麵)
5. 顯示所有設定 (SHOW ALL SETTINGS)
顯示現在設定的條件，如果確定就可以開時搜尋了!
6. 開始搜尋 (START)
顯示機器人搜尋到的結果，搜尋完後仍可以更改條件繼續搜尋
若想要結束搜尋，請點選離開或輸入QUIT
7. 離開 (QUIT)
離開當前狀態，回到idle狀態。
            """
        elif state == 'get_location':
            info += """
您現在的狀態是:get_location
請傳送位置訊息(手機版)，設定成功時會再次顯示搜尋選單。
            """
        elif state == 'get_radius':
            info += """
您現在的狀態是:get_radius
請輸入搜尋半徑(公尺為單位)
設定成功時會再次顯示搜尋選單。
(注意: 設定需以">> "作為前綴符號)
(例如: >> 1000)
            """
        elif state == 'get_price_level':
            info += """
您現在的狀態是:get_price_level
請設定價錢標準(google map的標準)
設定成功時會再次顯示搜尋選單。
(注意: 請輸入">> 0~3"進行設定)
(例如: >> 1)
            """
        elif state == 'get_keyword':
            info += """
您現在的狀態是:get_keyword
請輸入關鍵字
設定成功時會再次顯示搜尋選單。
(注意: 設定需以">> "作為前綴符號)
(例如: >> 鍋燒意麵)
            """
        elif state == 'search_recipe':
            info += """
您現在的狀態是:search_recipe
選擇您想要的食譜類型
您可以使用以下的操作:
1. 點心與甜點 (GET DESSERT RECIPE)
2. 家常料理 (GET CUISINE RECIPE)
3. 異國料理 (GET EXOTIC RECIPE)
4. 冰品與飲品 (GET DRINK RECIPE)
5. 搜尋特定菜譜 (GET SPECIFIC RECIPE)
6. 離開 (QUIT)
            """
        elif state == 'dessert_recipe':
            info += """
您現在的狀態是:dessert_recipe
請選擇各種甜點類型
可選擇以下幾種
1. 隨機 (RANDOM)
2. 布丁 (PUDDING)
3. 巧克力 (CHOCOLATE)
4. 餅乾 (COOKIE)
5. 麵包 (BREAD)
(注意:可以連續搜尋，所以要結束搜尋的時候，請點選QUIT離開甜點食譜的搜尋)
            """
        elif state == 'dish_recipe':
            info += """
您現在的狀態是:dish_recipe
請選擇各種家庭料理
可選擇以下幾種
1. 隨機 (RANDOM)
2. 牛肉 (BEEF)
3. 豬肉 (PORK)
4. 雞肉 (CHICKEN)
5. 海鮮 (SEAFOOD)
6. 蛋 (EGG)
7. 蔬菜 (VEGETABLE)
(注意:可以連續搜尋，所以要結束搜尋的時候，請點選QUIT離開家庭料理食譜的搜尋)
            """
        elif state == 'exotic_recipe':
            info += """
您現在的狀態是:exotic_recipe
請選擇各種異國料理
可選擇以下幾種
1. 日式 (JAPANESE)
2. 美式 (AMERICAN)
3. 韓式 (KOREAN)
4. 義式 (ITALIAN)
5. 泰式 (THAI)
(注意:可以連續搜尋，所以要結束搜尋的時候，請點選QUIT離開異國料理食譜的搜尋)
            """
        elif state == 'drink_recipe':
            info += """
您現在的狀態是:drink_recipe
請選擇各種飲品或配料
可選擇以下幾種
1. 配料 (TOPPINGS)
2. 飲品 (DRINK)
3. 冰品 (ICE)
(注意:可以連續搜尋，所以要結束搜尋的時候，請點選QUIT離開飲品或配料的搜尋)
            """
        elif state == 'wait_target_recipe':
            info += """
您現在的狀態是:wait_target_recipe
請輸入您想要搜尋的類型
(注意: 設定需以">> "作為前綴符號)
(例如: >> 三杯雞)
(注意:可以連續搜尋，所以要結束搜尋的時候，請點選QUIT離開飲品或配料的搜尋)
            """
        elif state == 'help':
            info += """
您現在的狀態是:help
請離開(QUIT)來退出當前狀態!
            """
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
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定位置訊息成功!'))
        show_search_filter(event)

        return True
    return False


def get_the_radius(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'radius', int(tmp[1]))
            # update_state(get_id(event), 'state', 'search_filter')
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定搜索半徑成功!'))
            show_search_filter(event)
            return True
    return False


def get_the_price_level(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'min_p', int(tmp[1]))
            # update_state(get_id(event), 'state', 'search_filter')
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定價錢標準成功!'))
            show_search_filter(event)
            return True
    return False


def get_the_keyword(event):
    if event.message.type == 'text':
        tmp = event.message.text.split(" ")
        if len(tmp) > 1 and tmp[0] == '>>':
            update_state(get_id(event), 'key_w', tmp[1])
            # update_state(get_id(event), 'state', 'search_filter')
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定關鍵字成功!'))
            show_search_filter(event)
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
