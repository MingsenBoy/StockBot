from linebot.models import *
from bs4 import BeautifulSoup
import requests
import re
from stock import *
import pandas as pd

def base_3(message):
    target = message[:4]
    stock_n = message[5:]
    if not re.match(r"[+-]?\d+$", stock_n):
        stock_n = stock_change(stock_n)
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
    df_4 = df_3[df_3["有價證券代號"] == str(stock_n)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1]
    url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=' + str(stock_n)
    }
    data = {
        "STEP": "DATA",
        "STOCK_ID": str(stock_n),
        "RPT_CAT": "XX_M_YEAR"
    }
    res = requests.post(url,headers = headers,data = data)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    if re.match("獲利能力",target): 
        soup_t1 = soup.find_all("tr",{"class":"bg_h1 fw_normal"})[0]
        title = soup_t1.find_all("nobr")[:4]
        soup1 = soup.find_all("tr",{"bgcolor":"white"})
        a = soup1[0].find_all("nobr")[:4]  #毛利率
        b = soup1[1].find_all("nobr")[:4] #營業利益率
        c = soup1[3].find_all("nobr")[:4] #稅後淨利率
        d = soup1[6].find_all("nobr")[:4] #EPS
        e = soup1[8].find_all("nobr")[:4] #ROE
        f = soup1[9].find_all("nobr")[:4] #ROA
        message = FlexSendMessage(
            alt_text = '獲利能力',
            contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": str(title_),
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": str(title[0].text),
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "期別",
                            "size": "xl",
                            "color": "#000000",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(title[3].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[2].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[1].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        }
                        ],
                        "spacing": "xl",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(a[0].text),
                            "size": "md",
                            "color": "#555555",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(a[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "spacing": "none",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(b[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(b[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(c[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(c[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(d[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(d[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(e[0].text),
                        "size": "md",
                        "color": "#555555",
                        "margin": "none",
                        "align": "start",
                        "gravity": "center",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": str(e[3].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(e[2].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(e[1].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "size": "md",
                        "color": "#555555",
                        "margin": "none",
                        "align": "start",
                        "gravity": "center",
                        "wrap": True,
                        "text": str(f[0].text)
                    },
                    {
                        "type": "text",
                        "text": str(f[3].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(f[2].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(f[1].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    }
                    ],
                    "margin": "md"
                }
                ],
                "margin": "none",
                "spacing": "none",
                "borderWidth": "none",
                "cornerRadius": "none"
            },
            "styles": {
                "footer": {
                "separator": True
                }
            }
            }
        )
        return message
    elif re.match("償債能力",target):
        soup_t1 = soup.find_all("tr",{"class":"bg_h1 fw_normal"})[6]
        title = soup_t1.find_all("nobr")[:4]
        soup1 = soup.find_all("tr",{"bgcolor":"white"})
        a = soup1[51].find_all("nobr")[:4]  #速動比
        b = soup1[52].find_all("nobr")[:4] #流動比
        c = soup1[53].find_all("nobr")[:4] #利息保障倍數
        d = soup1[54].find_all("nobr")[:4] #現金流量比
        message = FlexSendMessage(
            alt_text = '獲利能力',
            contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": str(title_),
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": str(title[0].text),
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "期別",
                            "size": "xl",
                            "color": "#000000",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(title[3].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[2].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[1].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        }
                        ],
                        "spacing": "xl",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(a[0].text),
                            "size": "md",
                            "color": "#555555",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(a[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "spacing": "none",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(b[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(b[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(c[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(c[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(d[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(d[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    }
                    ]
                }
                ],
                "margin": "none",
                "spacing": "none",
                "borderWidth": "none",
                "cornerRadius": "none"
            },
            "styles": {
                "footer": {
                "separator": True
                }
            }
            }
        )
        return message
    elif re.match("經營能力",target):
        soup_t1 = soup.find_all("tr",{"class":"bg_h1 fw_normal"})[7]
        title = soup_t1.find_all("nobr")[:4]
        soup1 = soup.find_all("tr",{"bgcolor":"white"})
        a = soup1[57].find_all("nobr")[:4]  #應收帳款週轉率
        b = soup1[59].find_all("nobr")[:4] #應付帳款週轉率
        c = soup1[61].find_all("nobr")[:4] #存貨週轉率
        d = soup1[63].find_all("nobr")[:4] #固定資產週轉率
        e = soup1[64].find_all("nobr")[:4] #總資產週轉率
        message = FlexSendMessage(
            alt_text = '獲利能力',
            contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": str(title_),
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": str(title[0].text),
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "期別",
                            "size": "xl",
                            "color": "#000000",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(title[3].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[2].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(title[1].text),
                            "size": "xl",
                            "color": "#000000",
                            "align": "center",
                            "weight": "bold",
                            "gravity": "center",
                            "wrap": True
                        }
                        ],
                        "spacing": "xl",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(a[0].text),
                            "size": "md",
                            "color": "#555555",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(a[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(a[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "spacing": "none",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(b[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(b[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(b[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(c[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(c[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(c[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": str(d[0].text),
                            "size": "md",
                            "color": "#555555",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": str(d[3].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[2].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(d[1].text),
                            "size": "lg",
                            "color": "#111111",
                            "align": "center",
                            "gravity": "center"
                        }
                        ],
                        "margin": "md"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": str(e[0].text),
                        "size": "md",
                        "color": "#555555",
                        "margin": "none",
                        "align": "start",
                        "gravity": "center",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": str(e[3].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(e[2].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    },
                    {
                        "type": "text",
                        "text": str(e[1].text),
                        "size": "lg",
                        "color": "#111111",
                        "align": "center",
                        "gravity": "center"
                    }
                    ],
                    "margin": "md"
                }
                ],
                "margin": "none",
                "spacing": "none",
                "borderWidth": "none",
                "cornerRadius": "none"
            },
            "styles": {
                "footer": {
                "separator": True
                }
            }
            }
        )
        return message