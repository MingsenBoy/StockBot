import requests
import inspect
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

# 爬蟲個股行情
def price(stock):
    response = requests.get(
        url=f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock}").json()
    data = response['data'][-1]
    result = inspect.cleandoc(f"""日期：{data[0]}
                                成交股數：{data[1]}
                                成交金額：{data[2]}
                                開盤價：{data[3]}
                                最高價：{data[4]}
                                最低價：{data[5]}
                                收盤價：{data[6]}
                                漲跌價差：{data[7]}
                                成交筆數：{data[8]}""")
    return result


# 爬蟲基本面資訊
def fundamental(stock):
    response = requests.get(
        url=f"http://www.twse.com.tw/exchangeReport/BWIBBU?response=json&stockNo={stock}").json()
    data = response['data'][-1]
    result = inspect.cleandoc(f"""日期：{data[0]}
                                殖利率(%)：{data[1]}
                                股利年度：{data[2]}
                                本益比：{data[3]}
                                股價淨值比：{data[4]}
                                財報年/季：{data[5]}""")
    return result


# 爬蟲即時新聞
def news_crawler():
    base = "https://news.cnyes.com"
    url = "https://news.cnyes.com/news/cat/headline"
    re = requests.get(url)

    content = ""

    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("a", {"class": "_1Zdp"})

    for index, d in enumerate(data):
        if index < 8:
            title = d.text
            href = base + d.get("href")
            content += "{}\n{}\n".format(title, href)
        else:
            break

    return content


# 爬蟲大盤
def stock_index():
    response = requests.get(
        url="http://www.twse.com.tw//indicesReport/MI_5MINS_HIST").json()
    data = response['data'][-1]
    result = inspect.cleandoc(f"""日期：{data[0]}
                                開盤指數：{data[1]}
                                最高指數：{data[2]}
                                最低指數：{data[3]}
                                收盤指數：{data[4]}""")
    return result


# 爬蟲法人買賣超
def institution(stock):
    day = date.today()
    if day.weekday() == 5:
        day -= timedelta(days=1)
    elif day.weekday() == 6:
        day -= timedelta(days=2)

    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
        "dataset": "InstitutionalInvestorsBuySell",
        "stock_id": stock,
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

# 操作教學
def help():
    result = inspect.cleandoc(f"""[操作教學]
                                P+個股代號：當日個股行情
                                F+個股代號：基本面資訊
                                T+個股代號：外資買賣超
                                新聞：即時新聞清單
                                大盤：當日大盤行情""")
    return result