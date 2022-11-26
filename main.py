import os
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
    carousel_images
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    token = event.reply_token
    msg = event.message.text

    # idle state
    if msg == 'WAITERIAN':
        line_bot_api.reply_message(
            token,
            FlexSendMessage(
                alt_text = 'WAITERIAN',
                contents = carousel_images
            )
        )

    if msg == 'FOOD':
        line_bot_api.reply_message(token, TextSendMessage(text='I get FOOD'))
    if msg == 'ROULETTE':
        line_bot_api.reply_message(token, TextSendMessage(text='I get ROULETTE'))
    if msg == 'INFORMATION':
        line_bot_api.reply_message(token, TextSendMessage(text='I get INFORMATION'))
    if msg == 'ID':
        print(event)
        # line_bot_api.reply_message(token, TextSendMessage(text=f'User ID: {event.source.userId}'))
        # line_bot_api.reply_message(token, TextSendMessage(text=f'Group ID: {event.source.groupId}'))





if __name__ == "__main__":
    load_dotenv()
    app.run()
