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
import arrow
import numpy as np

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
                label="不用了", 
                text="退出" 
            ) 
        ]    
    ) )
    return(confirm_template_message)