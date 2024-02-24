from flask import Flask, request,send_from_directory
import requests
import finnhub
from datetime import *; from dateutil.relativedelta import *
import calendar

app = Flask(__name__)


@app.route('/')
def DisplayWeb():
    return send_from_directory('','home.html')

@app.route('/GetFormData/<string:ticker>')
def GetFormData(ticker):
    stock = ticker
    # make api call on the stock symbol
    today = date.today()
    From = today + relativedelta(months=-1)
    #finnhub requests
    finnhub_client = finnhub.Client(api_key="cn9qcdhr01qjv5iotqe0cn9qcdhr01qjv5iotqeg")
    profile = finnhub_client.company_profile2(symbol = ticker)
    found = {"found":0}
    if(len(profile) == 0):
        return found
    
    found["found"] = 1
    quote = finnhub_client.quote(stock)
    recommendation = finnhub_client.recommendation_trends(stock)
    news = finnhub_client.company_news(stock, _from=From, to=today)
    cnt = 0
    result = dict(list(profile.items()) + list(quote.items())+ list(recommendation[0].items()))
    for item in news:
        if(item["image"] != "" and item["url"] != "" and item["headline"]!="" and item["datetime"]!=""):
            cnt +=1
            imgKey = "image" + str(cnt)
            urlKey = "url" + str(cnt)
            headlineKey = "headline" + str(cnt)
            dateTimeKey = "datetime" + str(cnt)
            dateTimeValue = datetime.fromtimestamp(item["datetime"]).strftime("%d %b, %Y")
            news_dict = {imgKey:item["image"],urlKey:item["url"],headlineKey:item["headline"],dateTimeKey:dateTimeValue}
            result.update(news_dict)
        if(cnt == 5):
            break

    #polygon requests
    sixMonthAgo = today + relativedelta(months=-6,days=-1)
    chartsUrl = "https://api.polygon.io/v2/aggs/ticker/"+stock.upper()+"/range/1/day/" + sixMonthAgo.strftime("%Y-%m-%d") + "/" + today.strftime("%Y-%m-%d") + "?adjusted=true&sort=asc&apiKey=8DqA9QuyKALdfAB0CiZUO3mLRXyyx05H" 
    chartRes = requests.get(chartsUrl).json()
    # print("result length: " + str(len(chartRes["results"])))
    chartDict = {"results": chartRes["results"]}
    result.update(chartDict)
    result.update(found)
    return result

def GetStockInfo(stock):
    print(stock)
    today = date.today()
    From = today + relativedelta(months=-1)

    #finnhub requests
    finnhub_client = finnhub.Client(api_key="cn9qcdhr01qjv5iotqe0cn9qcdhr01qjv5iotqeg")
    profile = finnhub_client.company_profile2(symbol=stock)
    found = {"found":0}
    if(len(profile) == 0):
        return found
    
    found["found"] = 1
    quote = finnhub_client.quote(stock)
    recommendation = finnhub_client.recommendation_trends(stock)
    news = finnhub_client.company_news(stock, _from=From, to=today)
    cnt = 0
    result = dict(list(profile.items()) + list(quote.items())+ list(recommendation[0].items()))
    for item in news:
        if(item["image"] != "" and item["url"] != "" and item["headline"]!="" and item["datetime"]!=""):
            cnt +=1
            imgKey = "image" + str(cnt)
            urlKey = "url" + str(cnt)
            headlineKey = "headline" + str(cnt)
            dateTimeKey = "datetime" + str(cnt)
            dateTimeValue = datetime.fromtimestamp(item["datetime"]).strftime("%d %b, %Y")
            news_dict = {imgKey:item["image"],urlKey:item["url"],headlineKey:item["headline"],dateTimeKey:dateTimeValue}
            result.update(news_dict)
        if(cnt == 5):
            break

    #polygon requests
    sixMonthAgo = today + relativedelta(months=-6,days=-1)
    chartsUrl = "https://api.polygon.io/v2/aggs/ticker/"+stock.upper()+"/range/1/day/" + sixMonthAgo.strftime("%Y-%m-%d") + "/" + today.strftime("%Y-%m-%d") + "?adjusted=true&sort=asc&apiKey=8DqA9QuyKALdfAB0CiZUO3mLRXyyx05H" 
    chartRes = requests.get(chartsUrl).json()
    # print("result length: " + str(len(chartRes["results"])))
    chartDict = {"results": chartRes["results"]}
    result.update(chartDict)
    result.update(found)
    return result
    
if __name__=='__main__':
   app.run()