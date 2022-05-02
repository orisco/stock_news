import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "3OL0KMISIGCVY7YV"
NEWS_API_KEY = "78327e8eeb5a44f2a8b7b79e0dd6d913"

#Trilio
account_sid = 'ACd03498e74f1ce87d6de24c69038f87ec'
auth_token = 'e88b75def7d37e9f9b0163574dd4ed39'
client = Client(account_sid, auth_token)
my_phone = '+17473022311'

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
stock_open = float(data[list(data)[0]]['1. open'])
stock_close = float(data[list(data)[0]]['4. close'])

if stock_open > stock_close:
    difference = stock_open - stock_close
    stock_positive = False
else:
    difference = stock_close - stock_open
    stock_positive = True

percent_change = round((difference / stock_close) * 100, 2)

# if percent_change >= 5:
news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}
response = requests.get(url=NEWS_ENDPOINT, params=news_params)
data = response.json()['articles'][:3]

for news_article in data:
    source_name = news_article['source']['name']
    headline = news_article['title']
    brief = news_article['description']

    body = f"{STOCK}: {'🔺' if stock_positive else '🔻'}{percent_change}%\nHeadline: {headline}\nBrief: {brief}"


    message = client.messages \
        .create(
        body=body,
        from_=my_phone,
        to='+13109337464'
    )

