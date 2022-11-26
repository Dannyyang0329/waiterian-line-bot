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
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

from flex_message import (
    get_carousel_images_json, get_single_restaurant_json
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    token = event.reply_token
    msg = event.message.text

    cur_state = get_state(event)

    # idle state
    if msg == 'WAITERIAN':
        line_bot_api.reply_message(
            token,
            FlexSendMessage(
                alt_text = 'WAITERIAN',
                contents = get_carousel_images_json()
            )
        )

    if msg == 'FOOD':
        # line_bot_api.reply_message(token, TextSendMessage(text='I get FOOD'))
        response = get_restaurant (
            22.993,
            120.219,
            1000,
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
