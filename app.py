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

#*********function*****************
from stock_news import *
import test
from stock import *

#*********function*****************

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'I0L0HMlrOO5TGwEkQO/BXgiL0EhYKG6XKb0GXYNG3SzPypdSflkwO2pwqhArnyUVtlmrJwac40WQT1Fw/3CM91OlNVP9Cj5zSxKa5gM5+8K5nBUGrfO8FCBhJ3KQbI7jvBIbBJCGYhRv+GMND4BphQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('188aea8ff2896544e83136e56e2756c4')

line_bot_api.push_message('U066c7cf935fa7a185f301ca749aecc64', TextSendMessage(text = 
f"""[操作教學]
    P+個股代號：當日個股行情
    F+個股代號：基本面資訊
    T+個股代號：外資買賣超
    新聞：即時新聞清單
    股票股名:個股資訊或個股新聞
    大盤：當日大盤行情"""))
#請輸入欲查詢股票資料\n格式為---股票 股名

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
                #thumbnail_image_url = r"D:\NSYSU_CU\111-1\Fintech\picture\template_pic.png",
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
                    ),
                    MessageAction(
                        label= message[3:] + " 基本面資訊",
                        text= "基本面資訊 " + message[3:]
                    )
                ]
                ),
                CarouselColumn(
                #thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                title = message[3:] + " 股票資訊",
                text ="請點選想查詢的股票資訊",
                actions =[
                    MessageAction(
                        label= message[3:] + " 外資買賣超",
                        text= "外資買賣超 " + message[3:]
                    ),
                    MessageAction(
                        label= message[3:] + " 最新分鐘圖",
                        text= "最新分鐘圖 " + message[3:]
                    ),
                    MessageAction(
                        label= message[3:] + " 日線圖",
                        text= "日線圖 " + message[3:]),
                ]
                ),
                CarouselColumn(
                #thumbnail_image_url = r"D:\NSYSU_CU\111-1\Fintech\picture\template_pic.png",
                title = message + "股利資訊",
                text = "請點選想查詢的股票資訊",
                actions = [
                    MessageAction(
                        label = message[3:] + " 平均股利",
                        text= "平均股利 " + message[3:]
                    ),
                    MessageAction(
                        label= message[3:] + " 歷年股利",
                        text= "歷年股利 " + message[3:]
                    ),
                    MessageAction(
                        label= message[3:] + " 基本面資訊",
                        text= "基本面資訊 " + message[3:]
                    )
                ]
                ),
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif '大戶籌碼 ' in message:
        flex_message = TextSendMessage(text="請選擇要顯示的買賣超資訊",
                                       quick_reply=QuickReply(
                                        items=[
                                            QuickReplyButton(action=MessageAction(label="最新法人", text="最新法人買賣超 " + message[5:])),
                                            QuickReplyButton(action=MessageAction(label="歷年法人", text="歷年法人買賣超 " + message[5:])),
                                            QuickReplyButton(action=MessageAction(label="外資", text="外資買賣超 " + message[5:])),
                                            QuickReplyButton(action=MessageAction(label="投信", text="投信買賣超 " + message[5:])),
                                            QuickReplyButton(action=MessageAction(label="自營商", text="自營商買賣超 " + message[5:])),
                                            QuickReplyButton(action=MessageAction(label="三大法人", text="三大法人買賣超 " + message[5:]))
                                        ]
                                       )  
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    # elif "股票 " in message:
    #     stock_mes = stock_message(message[3:])
    #     line_bot_api.reply_message(event.reply_token,stock_mes)
    elif "個股資訊 " in message:
        stock_n = stock_id(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_n),cont])

    elif "個股新聞 " in message:
        new_one = one_new(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[new_one,cont])

    elif "基本面資訊 " in message:
        fundamental = fundamental_(message[6:])
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(fundamental),cont])
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(test.fundamental(message)))

    elif "外資買賣超 " in message:
        institution = institution_(message[6:])
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(institution),cont])
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(test.fundamental(message)))

    elif "最新分鐘圖 " in message:
        m = min_close(message[6:])
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[m,cont])

    elif "日線圖 " in message:
        d = stock_day(message[4:])
        cont = continue_after(message[4:])
        line_bot_api.reply_message(event.reply_token,[d,cont])

    elif "平均股利 " in message:
        contiun = contiun_dividend(message[5:])
        dividend_one = average_dividend(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(contiun),dividend_one,cont])
            
    elif "歷年股利 " in message:
        dividend_year = year_dividend(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[dividend_year,cont]) 

    elif re.match("新聞",message):
        news = stock_new()
        line_bot_api.reply_message(event.reply_token,news)
    elif re.match("頭條新聞",message):
        news = headlines()
        line_bot_api.reply_message(event.reply_token,news)
    elif re.match("台股新聞",message):
        news = tw_stock()
        line_bot_api.reply_message(event.reply_token,news)
    elif re.match("國際新聞",message):
        news = wd_stock()
        line_bot_api.reply_message(event.reply_token,news)


    # In[]
    elif "P" in message:
        message = message.replace("P", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.price(message)))
    # 基本面分析
    elif "F" in message:
        message = message.replace("F", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.fundamental(message)))
    # # 即時新聞
    # elif "新聞" in message:
    #     result = test.news_crawler()
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 當日大盤
    elif "大盤" in message:
        result = test.stock_index()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 外資買賣超
    elif "T" in message:
        message = message.replace("T", "")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.institution(message)))
    # elif "help" in message:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(test.help()))
    else:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入help可參照輸入格式"))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.help()))





#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    app.run(host='0.0.0.0', port=port)