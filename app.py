#載入LineBot所需要的模組
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re 

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'I0L0HMlrOO5TGwEkQO/BXgiL0EhYKG6XKb0GXYNG3SzPypdSflkwO2pwqhArnyUVtlmrJwac40WQT1Fw/3CM91OlNVP9Cj5zSxKa5gM5+8K5nBUGrfO8FCBhJ3KQbI7jvBIbBJCGYhRv+GMND4BphQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('188aea8ff2896544e83136e56e2756c4')

line_bot_api.push_message('U066c7cf935fa7a185f301ca749aecc64', TextSendMessage(text = '請輸入欲查詢股票資料/格式為---股票-股名'))


# 監聽所有來自 /callback 的 Post Request
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


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)
    message = text=event.message.text
    #line_bot_api.reply_message(event.reply_token,message)
    if re.match('股票',message):
        buttons_template_message = TemplateSendMessage(
        alt_text = "股票資訊",
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                thumbnail_image_url = r"D:\NSYSU_CU\111-1\Fintech\picture\template_pic.png",
                title = message + "股票資訊",
                text = "請點選想查詢的股票資訊",
                actions = [
                    MessageAction(
                        label = message[3:] + " 個股資訊",
                        text= "個股資訊 " + message[3:]
                    ),
                    MessageAction(
                        label= message[3:] + " 個股新聞",
                        text= "個股新聞 " + message[3:]
                    )
                ]
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請參照正確格式"))
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入欲查詢股票資料/格式為---股票-股名"))



# @handler.add(MessageEvent, message=TextMessage) 
# def handle_message(event):
# 　　message = event.message.text
# 　　if re.match("你是誰",message):
# 　　　　line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~"))
# 　　else:
# 　　　　line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)