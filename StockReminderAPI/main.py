import os
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

message = ""

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": os.environ["API_KEY_STOCK"],
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()

stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

stock_yesterday = float(stock_data_list[0]["4. close"])
stock_before_yesterday = float(stock_data_list[1]["4. close"])

difference_in_price = (abs(stock_before_yesterday - stock_yesterday)/stock_yesterday)*100

if stock_yesterday > stock_before_yesterday:
    message += f"🔼 {difference_in_price}% TSLA\n"
elif stock_yesterday < stock_before_yesterday:
    message += f"🔽 {difference_in_price}% TSLA\n"
else:
    message += f"⏯️ Nothing changed TSLA\n"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": os.environ["API_KEY_NEWS"]
}

response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
response.raise_for_status()

data_news = response.json()["articles"][0]
news_title = data_news["title"]
news_description = data_news["description"]

message += f"Headline: {news_title}\nDescription: {news_description}"
print(message)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

account_sid = '***'
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='***',
    body=message,
    to='***'
    )

print(message.sid)

