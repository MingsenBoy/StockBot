import requests
from bs4 import BeautifulSoup 
from linebot.models import *
import pandas as pd

# In[]
def headlines():
    headers = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }  
    title_list = []
    link_list = []

    base_url = "https://news.cnyes.com/"
    url = "https://news.cnyes.com/news/cat/headline"
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text,"lxml")
    titles = soup.find_all("a",{'class':'_1Zdp'})
    
    for i in range(0,10):
        title_list.append((titles[i]).get('title'))
        link = base_url + (titles[i]).get('href') 
        link_list.append(link)

    message = FlexSendMessage(
        alt_text = '頭條新聞',
        contents = {
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": "https://campaign.cnyes.com/topics/anuesns/images/logo-dark.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "fit",
        "margin": "none"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
            {
                "type": "text",
                "text": "財經新聞",
                "wrap": True,
                "weight": "bold",
                "gravity": "center",
                "size": "3xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[0]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[0])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[1]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[1])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[2]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[2])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[3]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[3])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[4]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[4])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[5]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[5])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[6]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[6])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[7]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[7])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[8]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[8])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title_list[9]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(link_list[9])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                }
                ]
            }
            ],
            "margin": "none"
        }
        }
    )
    return message

# In[]
def tw_stock():
    url = "https://news.cnyes.com/news/cat/tw_stock"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("a",{"class":"_1Zdp"},limit = 10)
    base = "https://news.cnyes.com"
    title = []
    address = []
    for i in soup1:
        title.append(i.get("title"))
        address.append(base + i.get("href"))
    message = FlexSendMessage(
        alt_text = '台股新聞',
        contents = {
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": "https://campaign.cnyes.com/topics/anuesns/images/logo-dark.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "fit",
        "margin": "none"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
            {
                "type": "text",
                "text": "財經新聞",
                "wrap": True,
                "weight": "bold",
                "gravity": "center",
                "size": "3xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[0]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[0])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[1]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[1])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[2]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[2])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[3]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[3])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[4]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[4])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[5]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[5])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[6]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[6])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[7]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[7])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[8]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[8])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[9]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[9])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                }
                ]
            }
            ],
            "margin": "none"
        }
        }
    )
    return message

def wd_stock():
    url = "https://news.cnyes.com/news/cat/wd_stock"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("a",{"class":"_1Zdp"},limit = 10)
    base = "https://news.cnyes.com"
    title = []
    address = []
    for i in soup1:
        title.append(i.get("title"))
        address.append(base + i.get("href"))
    message = FlexSendMessage(
        alt_text = '國際新聞',
        contents = {
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": "https://campaign.cnyes.com/topics/anuesns/images/logo-dark.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "fit",
        "margin": "none"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
            {
                "type": "text",
                "text": "財經新聞",
                "wrap": True,
                "weight": "bold",
                "gravity": "center",
                "size": "3xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[0]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[0])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[1]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[1])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[2]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[2])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[3]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[3])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[4]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[4])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[5]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[5])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[6]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[6])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[7]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[7])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[8]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[8])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "◆" + str(title[9]),
                        "color": "#0066FF",
                        "size": "lg",
                        "flex": 1,
                        "action": {
                        "type": "uri",
                        "label": "action",
                        "uri": str(address[9])
                        },
                        "wrap": True
                    }
                    ],
                    "margin": "none"
                }
                ]
            }
            ],
            "margin": "none"
        }
        }
    )
    return message

def stock_new():
    buttons_template_message = TemplateSendMessage( 
    alt_text = "股票新聞",
    template=ButtonsTemplate( 
        thumbnail_image_url="https://s.yimg.com/ny/api/res/1.2/RqETwlh8PY7yrbaDIhyxdQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM4MC40NDQ0NDQ0NDQ0NDQ0Ng--/https://s.yimg.com/uu/api/res/1.2/Vn5SfDtQIEZNmoxFT0hVQw--~B/aD0yMTQ7dz0zNjA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/zh-tw/cnyes.com.tw/bfd0fd8921c2a100ac91dab8014a84af",
        title="股市新聞", 
        text="請點選想查詢的新聞種類", 
        actions=[
            MessageAction( 
                label="頭條新聞 TOP10",
                text="頭條新聞"),
            MessageAction( 
                label="台股新聞 TOP10",
                text="台股新聞"),
            MessageAction( 
                label="國際新聞 TOP10",
                text="國際新聞"),    
            ] 
        ) 
    )
    return buttons_template_message