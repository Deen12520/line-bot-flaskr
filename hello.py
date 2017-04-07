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

channel_access_token = '9l5B7NQq8/JFiuQgPLYcmbmPP214CBwt5FLGfMKxXHjix/gdbOnldrMTtlXD6O2vAv2S8VmJUFCi3druYsrHCLSyWZsBwJPMYi/wNBFPVZCcaEHqpBF5Aj8yRQzy19qW9w0Sp9Oki8eFN+g/vhACfAdB04t89/1O/w1cDnyilFU='
channel_secret = '05ce501ae6e7f74c767dffea1444f06b'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='hello,'+event.message.text))

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Msg'))
    pass


if __name__ == "__main__":
    app.run()