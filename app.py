from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import re
import test


# 要先設定環境變數
app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['TOKEN'])
handler = WebhookHandler(os.environ['SECRET'])


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


# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當日行情
    message = event.message.text
    if "P" in message:
        message = message.replace("P", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.price(message)))
    # 基本面分析
    elif "F" in message:
        message = message.replace("F", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.fundamental(message)))
    # 即時新聞
    elif "新聞" in message:
        result = test.news_crawler()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 當日大盤
    elif "大盤" in message:
        result = test.stock_index()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 外資買賣超
    elif "T" in message:
        message = message.replace("T", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.institution(message)))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.help()))

    # 回覆文字
    # message = event.message.text
    # if re.match("你是誰",message):
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~"))
    # else:
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

    # 回覆圖片
    # if re.match('我誰', message):
    #     image_message = ImageSendMessage(
    #         original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
    #         preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
    #     )
    # line_bot_api.reply_message(event.reply_token, image_message)

    # 回覆面板
    # message = event.message.text
    # if "股票 " in message:
    #     buttons_template_message = TemplateSendMessage(
    #         alt_text="股票資訊",
    #         template=CarouselTemplate(
    #             columns=[
    #                 CarouselColumn(
    #                     thumbnail_image_url="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
    #                     title=message + " 股票資訊",
    #                     text="請點選想查詢的股票資訊",
    #                     actions=[
    #                         MessageAction(
    #                             label=message[3:] + " 個股資訊",
    #                             text="個股資訊 " + message[3:]),
    #                         MessageAction(
    #                             label=message[3:] + " 個股新聞",
    #                             text="個股新聞 " + message[3:])
    #                     ]
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, buttons_template_message)


# 主程式
#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 80))
#    app.run(host='0.0.0.0', port=port)