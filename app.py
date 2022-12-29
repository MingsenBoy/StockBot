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

import pyodbc

#*********function*****************
from stock_news import *
import test
from stock import *
from stock_list import *
from stock_base import * 
#*********function*****************


app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'I0L0HMlrOO5TGwEkQO/BXgiL0EhYKG6XKb0GXYNG3SzPypdSflkwO2pwqhArnyUVtlmrJwac40WQT1Fw/3CM91OlNVP9Cj5zSxKa5gM5+8K5nBUGrfO8FCBhJ3KQbI7jvBIbBJCGYhRv+GMND4BphQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('188aea8ff2896544e83136e56e2756c4')

line_bot_api.push_message('U066c7cf935fa7a185f301ca749aecc64', TextSendMessage(text = 
f"""[請使用關鍵字]
大盤：當日大盤行情
新聞:查詢鉅亨網TOP10的頭條新聞、台股新聞、國際新聞
關注(取消關注) 股票名稱:ex. 關注(取消關注) 台積電 
查詢關注:檢視關注股票最新資訊
股票 股票名稱：進入個股資訊面板(ex. 股票 台積電)
大戶籌碼 股票名稱:該股票大戶籌碼相關資訊
""")
)
#請輸入欲查詢股票資料\n格式為---股票 股名

from flask import g
#呼叫程式碼時，都要先執行該段程式碼
@app.before_request
def before_request():
    connection_string = "Driver=SQL Server;Server=localhost;Database={0};Trusted_Connection=Yes;Database={0};" 
    g.cnxn = pyodbc.connect(connection_string.format("linebot"), autocommit=True)

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

#####
#新增股票到關注清單
def stock_database_add(message):
    try:
        stock_n = message
        stock_i = stock_change(message)
        sql = '''
            SELECT *
              FROM [linebot].[dbo].[Stocklist]
        '''
        print(sql)
        result = pd.read_sql(sql=sql, con=g.cnxn, coerce_float=True)
        if str(stock_i) not in result["Symbol"].values:
            Insert_sql = '''
                INSERT INTO Stocklist (Symbol,Name) VALUES (N'{}',N'{}')
            '''.format(stock_i,stock_n)
            print(Insert_sql)
            cursor = g.cnxn.cursor()
            cursor.execute(Insert_sql)
            cursor.commit()

            return stock_i + stock_n + " 已關注"
        else:
            return stock_i + stock_n + " 已是關注股票"
    except Exception as e:
        print(e)
        return "查無您輸入的訊息，請重新輸入確認"

#刪除股票清單中的股票
def stock_database_del(message):
    try:
        stock_n = message
        stock_i = stock_change(message)
        sql = '''
            SELECT *
              FROM [linebot].[dbo].[Stocklist]
        '''
        result = pd.read_sql(sql=sql, con=g.cnxn, coerce_float=True)
        if str(stock_i) in result["Symbol"].values:
            Insert_sql = '''
                DELETE FROM Stocklist WHERE Symbol = '{}'
            '''.format(stock_i)
            cursor = g.cnxn.cursor()
            cursor.execute(Insert_sql)
            cursor.commit()
            return stock_i + stock_n + " 已取消關注"
        else:
            return stock_i + stock_n + " 並非已關注股票"
    except:
        return "查無您輸入的訊息，請重新輸入"

#查詢清單
def find_list():
    sql = '''
       SELECT *
          FROM [linebot].[dbo].[Stocklist]
    '''
    result = pd.read_sql(sql=sql, con=g.cnxn, coerce_float=True)
    context = ""
    for i in range(len(result)):
        message = result['Symbol'].iloc[i]
        url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(message)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        res = requests.get(url,headers = headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
        soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
        soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
        soup4 = soup3.find("a").text.split("\xa0")
        soup_1 = soup.find("td",{"style":"padding:0 18px 5px 0;text-align:right;"})
        star = emoji.emojize(':small_blue_diamond:')
        #star_2 = emoji.emojize(':sunny:')
        context += "{} {} 最新資訊 \n-------------------------- \n{} {}\n{} 最新成交價 : {} \n{} 開盤價 : {} \n{} 最高價 : {} \n{} 最低價 : {} \n{} 漲跌幅 : {} \n--------------------------\n".format(soup4[0],soup4[1],star,soup_1.text,star,soup2[0],star,soup2[5],star,soup2[6],star,soup2[7],star,soup2[3])
    return context
#####

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
                        label= message[3:] + " 同業比較",
                        text= "同業比較 " + message[3:]
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
                        label= message[3:] + " 獲利能力",
                        text=  "獲利能力 " + message[3:]
                    )
                ]
                ),
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif '大戶籌碼' in message:
        st = message[5:]
        flex_message = TextSendMessage(text="請選擇要顯示的買賣超資訊", 
                                    quick_reply=QuickReply(items=[ 
                                        QuickReplyButton(action=MessageAction(label="最新法人", text="最新法人買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="歷年法人", text="歷年法人買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="外資", text="外資買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="投信", text="投信買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="自營商", text="自營商買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="三大法人", text="三大法人買賣超 " + st))
                                    ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif "最新法人買賣超 " in message:
        inv = investors(message[8:])
        cont = continue_after_BS(message[8:])
        line_bot_api.reply_message(event.reply_token,[inv,cont])

    elif "歷年法人買賣超 " in message:
        t_d = total_data(message[8:])
        cont = continue_after_BS(message[8:])
        line_bot_api.reply_message(event.reply_token,[t_d,cont])

    elif "外資買賣超 " in message:
        t_m = total_major(message[6:])
        f_i = foreign_inv(message[6:],t_m)
        cont = continue_after_BS(message[6:])
        line_bot_api.reply_message(event.reply_token,[f_i,cont])

    elif "投信買賣超 " in message:
        t_m = total_major(message[6:])
        c_i = credit_inv(message[6:],t_m)
        cont = continue_after_BS(message[6:])
        line_bot_api.reply_message(event.reply_token,[c_i,cont])

    elif "自營商買賣超 " in message:
        t_m = total_major(message[7:])
        s_i = self_employed_inv(message[7:],t_m)
        cont = continue_after_BS(message[7:])
        line_bot_api.reply_message(event.reply_token,[s_i,cont])  

    elif "三大法人買賣超 " in message:
        t_m = total_major(message[8:])
        m_i = major_inv(message[8:],t_m)
        cont = continue_after_BS(message[8:])
        line_bot_api.reply_message(event.reply_token,[m_i,cont])

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

    elif "同業比較 " in message:
        stock_one = compare_one(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_one),cont])

    elif "同業排名 " in message:
        stock_other = compare_other(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_other),cont])  

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
    
    elif "獲利能力 " in message:
        base = base_3(message)
        line_bot_api.reply_message(event.reply_token,base)

    elif re.match("查詢關注",message):
        find = find_list()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(find))

    elif "取消關注 " in message:
        delt = stock_database_del(message[5:])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(delt))

    elif "關注 " in message:
        add = stock_database_add(message[3:])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(add))

    # In[]
    # elif "P" in message:
    #     message = message.replace("P", "")
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(test.price(message)))
    # 基本面分析
    # elif "F" in message:
    #     message = message.replace("F", "")
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(test.fundamental(message)))
    # # 即時新聞
    # elif "新聞" in message:
    #     result = test.news_crawler()
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 當日大盤
    elif "大盤" in message:
        result = test.stock_index()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    # 外資買賣超
    # elif "T" in message:
    #     message = message.replace("T", "")
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(test.institution(message)))
    # elif "help" in message:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(test.help()))

    elif re.match("退出",message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("感謝您的使用~"))
    else:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage("輸入help可參照輸入格式"))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(test.help()))





#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    app.run(host='0.0.0.0', port=port)