from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#權杖
#access 存取 秘密
line_bot_api = LineBotApi('sZx+Zr8jrBYClnC1pKEEDWvCGw6aIuCOVaCtqVoVmjqKOjWRQxN++JWfWTdXuBdiego2q7EnpMno9EG3/KrTF002xlIJiPuzI5ETkUTYDjSPBt/HUwTQ+7jxYGjJTiS9iNCwbyXJyotsombUcd+pgQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ec46aa5d4801b2e52f28d799ee7b9379')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()