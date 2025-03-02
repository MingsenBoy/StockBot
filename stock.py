import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from linebot.models import *
import matplotlib.pyplot as plt
import pyimgur
import mpl_finance as mpf
import talib
import json
from random import choice
import time
from datetime import date
from datetime import timedelta
import arrow
import numpy as np
import inspect
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

chrome_options = Options()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument("--headless")
chrome_options.add_argument("disable-infobars")
chrome_options.add_experimental_option("prefs", { 
"profile.default_content_setting_values.notifications": 2
})

#股票名稱換代號
def stock_change(message):
    try:
        url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
        df = pd.read_html(requests.get(url).text)[0]
        df = df.iloc[:,2:7]
        df.columns = df.iloc[0,:]
        df = df[1:]
        url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
        df2 = pd.read_html(requests.get(url2).text)[0]
        df2 = df2.iloc[:,2:7]
        df2.columns = df2.iloc[0,:]
        df2 = df2[1:]
        df3 = pd.concat([df,df2])
        df4 = df3[df3["有價證券名稱"] == message]
        message = df4.values[0,0]
        return(message)
    except:
        return("請輸入正確的股票名稱")
        #return(message)


#個股資訊
def stock_id(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    try:
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
        soup_1 = soup.find("table",{"class":"b1 p4_4 r10"})
        soup_2 = soup_1.find_all("td",{"bgcolor":"white"})
        mes = "股票代號 :{} \n股票名稱 : {} \n產業別 : {} \n市場 : {}\n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {}  \n資本額 : {} \n市值 : {}".format(soup4[0],soup4[1],soup_2[1].text,soup_2[2].text,soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7],soup_2[4].text,soup_2[5].text)
        return mes
    except:
        return("請輸入正確的股票代號")


def message_split(message):
    message = message[6:]
    return message


# 爬蟲基本面資訊
def fundamental_(message):
    sto_number = stock_change(message)
    
    try:
        response = requests.get(
            url=f"http://www.twse.com.tw/exchangeReport/BWIBBU?response=json&stockNo={sto_number}").json()
        data = response['data'][-1]
        result = inspect.cleandoc(f"""日期：{data[0]}
                                    殖利率(%)：{data[1]}
                                    股利年度：{data[2]}
                                    本益比：{data[3]}
                                    股價淨值比：{data[4]}
                                    財報年/季：{data[5]}""")
        return result
    except:
        return("請輸入正確的股票代號")


# 爬蟲法人買賣超
def institution_(message):
    sto_number = stock_change(message)

    day = date.today()
    if day.weekday() == 5:
        day -= timedelta(days=2)
    elif day.weekday() == 6:
        day -= timedelta(days=3)
    else:
        day -= timedelta(days=1)

    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
        "dataset": "InstitutionalInvestorsBuySell",
        "stock_id": sto_number,
        "date": day,
    }
    response = requests.get(url, params=parameter)
    response = response.json()
    data = response['data'][-2]
    result = inspect.cleandoc(f"""日期：{day}
                                外資買進(股)：{data["buy"]:,}
                                外資賣出(股)：{data["sell"]:,}
                                外資買賣超(股)：{(data["buy"] - data["sell"]):,}""")
    return result


#個股新聞
def one_new(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/"+str(message) +  "/news"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("h3",{"class":"Mt(0) Mb(8px)"},limit = 13)
    address = []
    title = []
    for i in range(len(soup1)):
        if i != 1 and i != 5 and i != 9:
            new_ = soup1[i].find("a").get("href")
            address.append(new_)
            title.append(soup1[i].text)
    message = FlexSendMessage(
        alt_text = '頭條新聞',
        contents = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://s.yimg.com/os/creatr-uploaded-images/2020-04/a029d980-84ac-11ea-bc37-97373a02b37e",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "個股新聞",
                    "size": "3xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": "◆" + str(title[0]),
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0,
                            "size": "lg",
                            "color": "#0066FF",
                            "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": str(address[0])
                            },
                            "wrap": True
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[1]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[1])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[2]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[2])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[3]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[3])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[4]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[4])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[5]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[5])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[6]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[6])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[7]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[7])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[8]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[8])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "◆" + str(title[9]),
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0,
                                "size": "lg",
                                "color": "#0066FF",
                                "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": str(address[9])
                                },
                                "wrap": True
                            }
                            ]
                        }
                        ]
                    }
                    ]
                }
                ]
            }
            }
    )
    return message

#分鐘圖
def min_close(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;autoRefresh=1631105443818;symbols=%5B%22" + str(message) +".TW%22%5D;type=tick?bkt=tw-qsp-exp-no4&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor%2ChideMarketInfo&intl=tw&lang=zh-Hant-TW&partner=none&prid=3j6j761gjhcda&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1132&returnMeta=true"
    res = requests.get(url)
    jd = res.json()["data"][0]["chart"]["indicators"]["quote"][0]
    open_ = jd["open"]
    high = jd["high"]
    low = jd["low"]
    close = jd["close"]
    volume = jd["volume"]
    time = res.json()["data"][0]["chart"]["timestamp"]
    df = pd.DataFrame({"timestamp" :  time , "open" : open_ , "high" : high , "low" : low , "close" : close , "volume" : volume})
    time_ = pd.to_datetime(df["timestamp"] + 3600 * 8 , unit = "s")
    df["timestamp"] = time_
    df = df.fillna(method= "ffill")
    df = df[1:]
    jd_ = res.json()["data"][0]["chart"]["meta"]
    previousClose = jd_["previousClose"]
    close1 = []   #上漲
    close2 = []   #下跌
    for i in range(len(df)):
        if df["close"].values[i] >=  previousClose:
            close1.append(df["close"].values[i])
        else:
            close1.append(previousClose)
    for i in range(len(df)):
        if df["close"].values[i] <=  previousClose:
            close2.append(df["close"].values[i])
        else:
            close2.append(previousClose)
    df["close1"] = close1
    df["close2"] = close2
    df["Previous"] = previousClose
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == message]
    title = df_4.values[0,0] + " " + df_4.values[0,1]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.subplots(figsize=(15, 5)) 
    plt.title(title,fontsize = 15)
    plt.xlabel('時段',fontsize = 15)
    plt.ylabel('股價',fontsize = 15)
    plt.grid()
    plt.plot(df["timestamp"],df["close1"],"r")
    plt.plot(df["timestamp"],df["close2"],"g")
    plt.plot(df["timestamp"],df["Previous"],"yellow")
    plt.fill_between(df["timestamp"],df["close1"], df["Previous"], color = 'lightcoral')
    plt.fill_between(df["timestamp"],df["close2"], df["Previous"], color = 'palegreen')
    plt.savefig(str(message) + "分鐘圖.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "分鐘圖.png" #A Filepath to an image on your computer"
    title = str(message) + "分鐘圖"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#歷史股價資料
def stock_l(message):
    start = int(time.mktime(time.strptime(arrow.now().shift(months = 1).strftime("%Y-%m-%d"),"%Y-%m-%d")))
    end = int(time.mktime(time.strptime(arrow.now().shift(months = -3).strftime("%Y-%m-%d"),"%Y-%m-%d")))
    url = "https://ws.api.cnyes.com/ws/api/v1/charting/history?resolution=D&symbol=TWS:"+ message +":STOCK&from=" +str(start) + "&to="+str(end) + "&quote=1"
    res = requests.get(url)
    s = json.loads(res.text)
    t = []
    o = []
    h = []
    l = []
    c = []
    v = []
    name = [t,o,h,l,c,v]
    lis = ["t","o","h","l","c","v"]
    for n,lis in zip(name,lis):
        for d in (s["data"][lis]):
            n.append(d)
    df = pd.DataFrame({"日期":t,"開盤價":o,"最高價":h,"最低價":l,"收盤價":c,"成交量":v})    
    for i in range(len(df)):
        df["日期"][i] = time.strftime("%Y-%m-%d", time.localtime(df["日期"][i]))
    df.index = pd.to_datetime(df["日期"])
    df.index = df.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')) 
    df.drop("日期",axis = 1,inplace=True)
    df = df.sort_index()
    return df

#日線圖
def stock_day(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    df = stock_l(message)
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == message]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1]
    sma_10 = talib.SMA(np.array(df['最低價']), 10)
    sma_20 = talib.SMA(np.array(df['最低價']), 20)
    fig = plt.figure(figsize=(24, 15))
    ax = fig.add_axes([0,0.2,1,0.5])
    ax2 = fig.add_axes([0,0,1,0.2])
    ax.set_xticks(range(0, len(df.index),10))
    ax.set_title(title_,fontsize=30)
    ax.yaxis.set_tick_params(labelsize=15)
    ax.grid(True)
    ax.set_xticklabels(df.index[::10])
    mpf.candlestick2_ochl(ax, df['開盤價'], df['收盤價'], df['最高價'],
                        df['最低價'], width=0.6, colorup='r', colordown='g', alpha=0.75); 
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    ax.plot(sma_10, label='10日均線')
    ax.plot(sma_20, label='20日均線')
    mpf.volume_overlay(ax2, df['開盤價'], df['收盤價'], df['成交量'], colorup='r', colordown='g', width=0.5, alpha=0.8)
    ax2.grid(True)
    ax2.set_xticks(range(0, len(df.index), 10))
    ax2.set_xticklabels(df.index[::10])
    plt.xticks(rotation=45,fontsize=20)
    plt.yticks(fontsize=15)
    ax.legend(fontsize=20,loc = "upper left")
    plt.savefig(str(message) + "日線圖.png", bbox_inches = "tight") 
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "日線圖.png" #A Filepath to an image on your computer"
    title = str(message) + "日線圖"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message


def continue_after(message):
    if re.match(r"[+-]?\d+$", message):
        try:
            url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
            df = pd.read_html(requests.get(url).text)[0]
            df = df.iloc[:,2:7]
            df.columns = df.iloc[0,:]
            df = df[1:]
            url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
            df2 = pd.read_html(requests.get(url2).text)[0]
            df2 = df2.iloc[:,2:7]
            df2.columns = df2.iloc[0,:]
            df2 = df2[1:]
            df3 = pd.concat([df,df2])
            df4 = df3[df3["有價證券代號"] == message]
            message = df4.values[0,1]
        except:
            return("請輸入正確的股票代號")   
    confirm_template_message = TemplateSendMessage( 
    alt_text="繼續查詢", 
    template=ConfirmTemplate( 
        text="是否繼續查詢 " + message, 
        actions=[ 
            MessageAction( 
                label="繼續", 
                text="股票 " + message 
            ),
            MessageAction( 
                label="退出", 
                text="退出" 
            ) 
        ]    
    ) )
    return(confirm_template_message)

#平均股利1
def contiun_dividend(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/dividend"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("p",{"class":"Mb(20px) Mb(12px)--mobile Fz(16px) Fz(18px)--mobile C($c-primary-text)"}).text
    return soup1

#平均股利2
def average_dividend(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=" + str(message)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers=headers )
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("tr",{"align":"center","bgcolor":"white"})
    title = ["類別","平均股利(元)","平均增減(元)","均填權息日數","平均殖利率(%)","連續分派年數"]
    content = pd.DataFrame()
    for i in range(4,7):
            soup2 = soup1[i].find_all("td")
            content = content.append([[soup2[0].text,soup2[1].text,soup2[2].text,soup2[3].text,soup2[4].text,soup2[7].text]])
    content.columns = title
    content.index = content["類別"]
    content.drop("類別",axis=1,inplace = True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('平均股利')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, content, loc='center')
    plt.savefig(str(message) + "平均股利.png", bbox_inches = "tight")
    CLIENT_ID = "50086aa149e4219"
    PATH = str(message) + "平均股利.png" #A Filepath to an image on your computer"
    title = str(message) + "平均股利"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

# #歷年股利
# def year_dividend(message):
#     if not re.match(r"[+-]?\d+$", message):
#         message = stock_change(message)
#     url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/dividend"
#     headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
#     }
#     res = requests.get(url,headers= headers)
#     while str(res) != "<Response [200]>":
#         res = requests.get(url,headers= headers)
#     soup = BeautifulSoup(res.text,"html.parser")
#     soup_period = soup.find_all("div",{"class" :"D(f) W(84px) Ta(start)"})[1:]
#     period = []
#     for i in soup_period:
#         period.append(i.text)
#     soup_dividend = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(62px)"})[3:]
#     cash_dividend = []
#     stock_dividend = []
#     Interest_days = []
#     for i in range(0,len(soup_dividend),2):
#         cash_dividend.append(soup_dividend[i].text)
#         stock_dividend.append(soup_dividend[i+1].text)
#         #Interest_days.append(soup_dividend[i+2].text)
#     soup_dividendinterest_date = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(70px)"})
#     soup_date = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(108px)"})[2:]
#     for i in soup_dividendinterest_date:
#         Interest_days.append(i[1].text)
#     Ex_dividend_date = []
#     Dividend_payment_date = []
#     for i in range(0,len(soup_date),2):
#         Ex_dividend_date.append(soup_date[i].text)
#         Dividend_payment_date.append(soup_date[i+1].text)
#     df = pd.DataFrame({"股利所屬期間":period,"現金股利":cash_dividend,"股票股利":stock_dividend,"填息天數":Interest_days,
#                        "除權息日":Ex_dividend_date,"股利發放日":Dividend_payment_date})
#     df.index = df["股利所屬期間"]
#     df.drop("股利所屬期間",axis = 1,inplace=True)
#     plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
#     plt.rcParams['axes.unicode_minus'] = False
#     plt.figure('歷年股利')            # 視窗名稱
#     plt.figure(dpi = 500)
#     ax = plt.axes(frame_on=False)# 不要額外框線
#     ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
#     ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
#     pd.plotting.table(ax, df, loc='center')
#     plt.savefig(str(message) + "歷年股利.png", bbox_inches = "tight")
#     CLIENT_ID = "50086aa149e4219"
#     PATH = str(message) + "歷年股利.png" #A Filepath to an image on your computer"
#     title = str(message) + "歷年股利"
#     im = pyimgur.Imgur(CLIENT_ID)
#     uploaded_image = im.upload_image(PATH, title=title)
#     image_message = ImageSendMessage( 
#         original_content_url= uploaded_image.link,
#         preview_image_url= uploaded_image.link)
#     return image_message

#歷年股利
def year_dividend(message):
    message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/dividend"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    #soup_period = soup.find_all("div",{"class" :"D(f) W(84px) Ta(start)"})[1:]
    list_n = soup.find("div",{"class":"table-body-wrapper"}).find_all("li",{"class":"List(n)"})
    #print(list_n)
    data_all = []
    for i in  range(len(list_n)):
        period = list_n[i].find("div",{"class":"D(f) W(84px) Ta(start)"}).text
        dividend = list_n[i].find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(62px)"})
        cash_dividend = dividend[0].text
        stock_dividend = dividend[1].text
        days = list_n[i].find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(108px)"})
        ex_dividend_date  = days[0].text
        ex_rights_date = days[1].text
        cash_payment_date = days[2].text
        stock_payment_date = days[3].text
        interest_date = list_n[i].find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(70px)"})
        interest_date = interest_date[1].text
        data_one = {
            "股利所屬期間" : period,
            "現金股利" : cash_dividend,
            "股票股利" : stock_dividend,
            "除息日" : ex_dividend_date,
            "除權日" : ex_rights_date,
            "現金股利發放日" : cash_payment_date,
            "股票股利發放日" : stock_payment_date,
            "填息天數" : interest_date
        }
        data_all.append(data_one)
    
    df = pd.DataFrame(data_all)
    df.index = df["股利所屬期間"]
    df.drop("股利所屬期間",axis = 1,inplace=True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('歷年股利')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, df, loc='center')
    plt.savefig(str(message) + "歷年股利.png", bbox_inches = "tight")
    CLIENT_ID = "50086aa149e4219"
    PATH = str(message) + "歷年股利.png" #A Filepath to an image on your computer"
    title = str(message) + "歷年股利"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    
    return image_message

#同業比較   
def compare_one(message):
    #headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    try:
        browser = webdriver.Chrome(r"D:\NSYSU_CU\111-1\Fintech\chromedriver.exe", options = chrome_options)
        browser.get("https://login.yahoo.com/?.src=twfinance&.intl=tw&.lang=zh-Hant-TW&.done=https%3A%2F%2Ftw.stock.yahoo.com%2Fquote%2F2330%2Fcompare&pspid=152952224&activity=ybar-signin")
        member_user=browser.find_element_by_name('username')   #找到填入帳號的空格
        member_user.clear()
        member_user.send_keys('')         #填入帳號
        member_next=browser.find_element_by_id('login-signin')  #找到確認按鈕
        member_next.click()                                    #點擊確認
        time.sleep(3)
        member_pass=browser.find_element_by_id('login-passwd')     #找到填入密碼的空格
        member_pass.send_keys('')                         #填入密碼
        member_signin=browser.find_element_by_id('login-signin')  #找到確認按鈕
        member_signin.click()                                    #點擊確認
        time.sleep(3)
        #message = stock_change(message)
        browser.get("https://tw.stock.yahoo.com/quote/" + str(message) +"/compare")
        soup = BeautifulSoup(browser.page_source,"lxml")
        soup1 = soup.find("a",{"class":"D(ib) Fz(14px) Lh(20px) C($c-button) Mb(20px) Mb(16px)--mobile C($c-active-text):h Td(n)"}).text
        soup2 = soup.find_all("span",{"class":"C(#000) Fz(24px) Fw(600)"})
        ranking = soup.find_all("span",{'class':'C(#000) Fz(24px) Fw(600)'})
        message = "{} \n近1年漲跌幅 : 第{}名 \n近1年每股盈餘 : 第{}名 \n近1年殖利率 : 第{}名 \n近1年本益比 : 第{}名 \n近5日法人買賣超 : 第{}名 \n近1月營收年增率 : 第{}名".format(soup1,soup2[0].text,soup2[1].text,soup2[2].text,soup2[3].text,soup2[4].text,soup2[5].text)
        return message
    except:
        url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/compare"
        res = requests.get(url)
        #browser.get("https://tw.stock.yahoo.com/quote/" + str(message) +"/compare")
        soup = BeautifulSoup(res.text,"lxml")
        soup1 = soup.find("a",{"class":"D(ib) Fz(14px) Lh(20px) C($c-button) Mb(20px) Mb(16px)--mobile C($c-active-text):h Td(n)"}).text
        soup2 = soup.find_all("span",{"class":"C(#000) Fz(24px) Fw(600)"})
        ranking = soup.find_all("span",{'class':'C(#000) Fz(24px) Fw(600)'})
        message = "{} \n近1年漲跌幅 : 第{}名 \n近1年每股盈餘 : 第{}名 \n近1年殖利率 : 第{}名 \n近1年本益比 : {} \n近5日法人買賣超 : {} \n近1月營收年增率 : {}".format(soup1,soup2[0].text,soup2[1].text,soup2[2].text,"防爬機制阻擋","防爬機制阻擋","防爬機制阻擋")
        return message
    #except:
        #return "防爬機制阻擋"


#同業排名
def compare_other(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/compare"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    compare = "股票代號 \t股票名稱 \t近一月漲跌幅 \n"
    stock_id = soup.find_all("span",{"class":"Fz(14px) C(#979ba7) Ell"})
    stock_name = soup.find_all("div",{"class":"Lh(20px) Fw(600) Fz(16px) Ell"})
    stock_quote = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(100px) Bgc(t)"})
    stock_ud = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(100px) Bgc(t)"})[:-1]
    for i in range(len(stock_id)):
        try:
            stock_mark = stock_ud[i].find("span",{"class":"Mend(4px) Bds(s)"}).get("style")
            if "#ff333a" in  stock_mark:
                ud = "+"
            else:
                ud = "-"
        except:
            ud = " "
        compare += "{} \t{} \t {}\t{} \n".format(stock_id[i].text,stock_name[i].text,ud,stock_quote[i].text)
    return compare

#最新三大法人買賣超
def investors(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/institutional-trading"    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("div",{"style":"padding:0 12px 0 0"})[0:4]
    name = []
    buy = []
    sell = []
    b_s = []
    contuin = []
    for i in soup1:
        soup2 = i.find_all("span")
        name.append(soup2[0].text)
        buy.append(soup2[1].text)
        sell.append(soup2[2].text)
        b_s.append(soup2[3].text)
        contuin.append(soup2[4].text)
    df = pd.DataFrame({"單位(張)":name,"買進":buy,"賣出":sell,"買賣超":b_s,"連續買賣超":contuin})
    df.index = df["單位(張)"]
    df.drop("單位(張)",axis = 1,inplace = True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('最新法人買賣超')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, df, loc='center')
    plt.savefig(str(message) + "最新法人買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "最新法人買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "最新法人買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#歷年三大法人
def total_major(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/institutional-trading"
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("div",{"style":"padding:0 12px 0 0"})[4:]
    date = []
    foreign_inv = []
    credit = []
    self_employed = []
    total = []
    foreign_sharehold = []
    for i in soup1:
        soup2 = i.find_all("div")[:7]
        date.append(soup2[1].text)
        foreign_inv.append(soup2[2].text)
        credit.append(soup2[3].text)
        self_employed.append(soup2[4].text)
        total.append(soup2[5].text)
        foreign_sharehold.append(soup2[6].text)
    df = pd.DataFrame({"日期":date,"外資(張)":foreign_inv,"投信(張)":credit,"自營商(張)":self_employed,"合計(張)":total,"外資持股率(%)":foreign_sharehold})
    df.index = pd.to_datetime(df["日期"])
    df.index = df.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')) 
    df.drop("日期",axis = 1,inplace=True)
    int_ = ["外資(張)","投信(張)","自營商(張)","合計(張)"]
    for i in int_:
        df[i] = df[i].apply(lambda x: x.replace(",","")).astype("int64")
    df["外資持股率(%)"] = df["外資持股率(%)"].apply(lambda x: x.replace("%","")).astype(float)
    return df

#三大法人買賣超(資料)
def total_data(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    df = total_major(message)
    t = arrow.now().shift(months = -3).strftime("%Y-%m-%d")
    df = df.loc[:t].sort_index()
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('三大法人買賣超')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, df, loc='center')
    plt.savefig(str(message) + "三大法人.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "三大法人.png" #A Filepath to an image on your computer"
    title = str(message) + "三大法人"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#外資買賣超
def foreign_inv(message,t_m):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    s_p = stock_l(message)
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == str(message)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1] + "外資買賣"
    t = arrow.now().shift(months = -3).strftime("%Y-%m-%d")
    u = int(np.percentile(t_m["外資(張)"][t_m["外資(張)"] >= 0], [5]))
    p = int(np.percentile(t_m["外資(張)"][t_m["外資(張)"] <= 0], [50]))
    df2 = t_m.loc[:t].sort_index()
    df3 = s_p[t:]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    fig,ax = plt.subplots(figsize=(20, 5))
    ax.grid(True) 
    ax.set_title(title_,fontsize=15)
    ax.set_xticks(range(0, len(df3.index), 5))
    plt.xticks(rotation=45,fontsize=10)
    ax.bar(df2.index,df2["外資(張)"],color = "dodgerblue",label = "外資買賣超")
    ax.legend(loc = "upper left")
    for a,b,c in zip(df2.index,df2["外資(張)"],range(len(df2.index))):
        if c % 5 == 0 and b > 0:
            plt.text(a, b +u , '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "r")
        elif c % 5 == 0 and b < 0:
            plt.text(a, b + p, '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "darkgreen")
    ax2 = ax.twinx()
    ax2.set_xticks(range(0, len(df3.index), 5))
    ax2.plot(df3.index,df3["收盤價"],color = "orange",label = "股價")
    ax2.legend(loc = "lower left")
    plt.savefig(str(message) + "外資買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "外資買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "外資買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#投信買賣超
def credit_inv(message,t_m):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    s_p = stock_l(message)
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == str(message)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1] + "投信買賣"
    t = arrow.now().shift(months = -3).strftime("%Y-%m-%d")
    u = int(np.percentile(t_m["投信(張)"][t_m["投信(張)"] >= 0], [5]))
    p = int(np.percentile(t_m["投信(張)"][t_m["投信(張)"] <= 0], [50]))
    df2 = t_m.loc[:t].sort_index()
    df3 = s_p[t:]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    fig,ax = plt.subplots(figsize=(20, 5)) 
    plt.xticks(rotation=45,fontsize=10)
    ax.set_title(title_,fontsize=15)
    ax.set_xticks(range(0, len(df3.index), 5))
    ax.bar(df2.index,df2["投信(張)"],color = "rosybrown",label = "投信買賣超")
    ax.legend(loc = "upper left")
    for a,b,c in zip(df2.index,df2["投信(張)"],range(len(df2.index))):
        if c % 5 == 0 and b > 0:
            plt.text(a, b +u , '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "r")
        elif c % 5 == 0 and b < 0:
            plt.text(a, b + p, '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "darkgreen")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.set_xticks(range(0, len(df3.index), 5))
    ax2.plot(df3.index,df3["收盤價"],color = "orange",label = "股價")
    ax2.legend(loc = "lower left")
    plt.savefig(str(message) + "投信買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "投信買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "投信買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#自營商買賣超
def self_employed_inv(message,t_m):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    s_p = stock_l(message)
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == str(message)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1] + "自營商買賣超"
    t = arrow.now().shift(months = -3).strftime("%Y-%m-%d")
    u = int(np.percentile(t_m["自營商(張)"][t_m["自營商(張)"] >= 0], [5]))
    p = int(np.percentile(t_m["自營商(張)"][t_m["自營商(張)"] <= 0], [50]))
    df2 = t_m.loc[:t].sort_index()
    df3 = s_p[t:]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    fig,ax = plt.subplots(figsize=(15, 5)) 
    plt.xticks(rotation=45,fontsize=10)
    ax.set_title(title_,fontsize=15)
    ax.set_xticks(range(0, len(df3.index), 5))
    ax.bar(df2.index,df2["自營商(張)"],color = "orchid",label = "自營商買賣超")
    ax.legend(loc = "upper left")
    for a,b,c in zip(df2.index,df2["自營商(張)"],range(len(df2.index))):
        if c % 5 == 0 and b > 0:
            plt.text(a, b +u , '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "r")
        elif c % 5 == 0 and b < 0:
            plt.text(a, b + p, '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "darkgreen")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.set_xticks(range(0, len(df3.index), 5))
    ax2.plot(df3.index,df3["收盤價"],color = "orange",label = "股價")
    ax2.legend(loc = "lower left")
    plt.savefig(str(message) + "自營商買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "自營商買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "自營商買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#三大法人買賣超
def major_inv(message,t_m):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    s_p = stock_l(message)
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == str(message)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1] + "三大法人買賣"
    t = arrow.now().shift(months = -3).strftime("%Y-%m-%d")
    u = int(np.percentile(t_m["合計(張)"][t_m["合計(張)"] >= 0], [5]))
    p = int(np.percentile(t_m["合計(張)"][t_m["合計(張)"] <= 0], [50]))
    df2 = t_m.loc[:t].sort_index()
    df3 = s_p[t:]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    fig,ax = plt.subplots(figsize=(15, 5)) 
    plt.xticks(rotation=45,fontsize=10)
    ax.set_title(title_,fontsize=15)
    ax.set_xticks(range(0, len(df3.index), 5))
    ax.bar(df2.index,df2["自營商(張)"],color = "orchid",label = "自營商買賣超")
    ax.bar(df2.index,df2["投信(張)"],color = "rosybrown",label = "投信買賣超")
    ax.bar(df2.index,df2["外資(張)"],color = "dodgerblue",label = "外資買賣超")
    ax.legend(loc = "upper left")
    for a,b,c in zip(df2.index,df2["合計(張)"],range(len(df2.index))):
        if c % 5 == 0 and b > 0:
            plt.text(a, b + u , '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "r")
        elif c % 5 == 0 and b < 0:
            plt.text(a, b + p, '%.0f' % b, ha='center', va= 'bottom',fontsize=10,color = "darkgreen")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.set_xticks(range(0, len(df3.index), 5))
    ax2.plot(df3.index,df3["收盤價"],color = "orange",label = "股價")
    ax2.legend(loc = "lower left")
    plt.savefig(str(message) + "三大法人買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "三大法人買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "三大法人買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#繼續查詢(買賣超資訊)
def continue_after_BS(message):
    if re.match(r"[+-]?\d+$", message):
        try:
            url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
            df = pd.read_html(requests.get(url).text)[0]
            df = df.iloc[:,2:7]
            df.columns = df.iloc[0,:]
            df = df[1:]
            url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
            df2 = pd.read_html(requests.get(url2).text)[0]
            df2 = df2.iloc[:,2:7]
            df2.columns = df2.iloc[0,:]
            df2 = df2[1:]
            df3 = pd.concat([df,df2])
            df4 = df3[df3["有價證券代號"] == message]
            message = df4.values[0,1]
        except:
            return("請輸入正確的股票代號")   
    confirm_template_message = TemplateSendMessage( 
    alt_text="繼續查詢", 
    template=ConfirmTemplate( 
        text="是否繼續查詢 " + message + " 的買賣超資訊", 
        actions=[ 
            MessageAction( 
                label="繼續", 
                text="大戶籌碼 " + message 
            ),
            MessageAction( 
                label="退出", 
                text= "感謝您的使用~"
            ) 
        ]    
    ) )
    return(confirm_template_message)