import os
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
# 必須放上自己的Channel Secret
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

local_user = os.environ['LOCAL_USER_ID']
line_bot_api.push_message(local_user, TextSendMessage(text="Hello! Let's get start"))


# Monitor all callback Post Request
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

 
### Main function go to this code
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    