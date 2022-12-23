import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from utils import *
from fsm_controller import *

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


machines = {}

@handler.add(MessageEvent)
def handle_message(event):
    id = get_id(event)
    if id not in machines:
        machines.update({id: get_fsm('idle')})

    machines[id].advance(event)


if __name__ == "__main__":
    load_dotenv()
    app.run()
