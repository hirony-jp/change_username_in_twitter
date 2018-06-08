import json
import datetime as dt
import requests
from requests_oauthlib import OAuth1Session

def lambda_handler(event, context):

    # Open Weather Map API Key
    weather_key = ""

    # Twitter API Keys
    CK = ""
    CS = ""
    AT = ""
    ATS = ""
    twitter = OAuth1Session(CK, CS, AT, ATS)

    # config.
    city_name = "Matsue"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}&units=metric"
    weather_url = weather_url.format(city = city_name, key = weather_key)
    twitter_url = "https://api.twitter.com/1.1/account/update_profile.json"
    # AWS Lambda は UST なので JST に変えてやる必要がある
    now = dt.datetime.now()
    jst = now + dt.timedelta(hours=9)
    jst = jst.hour
    #username = "ひろにぃ@気温{temp}℃"
    username = "Hirony"

    # 天気データを取得
    weather_req = requests.get(weather_url)
    weather_data = json.loads(weather_req.text)
    weather_id = weather_data["weather"][0]["id"]
    #username = username.format(temp = weather_data["main"]["temp"])

    # weather id をもとに分類
    if weather_id == 800:
        if jst >= 18 and jst <= 23 or jst >= 0 and jst <= 5:
            username = username + "🌕"
        else:
            username = username + "☀"
    elif weather_id >= 801:
        if jst >= 18 and jst <= 23 or jst >= 0 and jst <= 5:
            username = username + "🌕☁"
        else:
            username = username + "☀☁"
    elif weather_id >= 802 and weather_id <= 804:
        username = username + "☁"
    elif weather_id >= 300 and weather_id <= 321:
        username = username + "🌂"
    elif weather_id >= 500 and weather_id <= 531:
        username = username + "☔"
    elif weather_id >= 200 and weather_id <= 232:
        username = username + "⚡☔"
    elif weather_id >= 600 and weather_id <= 622:
        username = username + "⛄"
    elif weather_id >= 900:
        username = username + "🌀"

    # set username parameter.
    params = { "name" : username }

    # update Twitter username.
    twitter_req = twitter.post(twitter_url, params = params)

    # respons check.
    if twitter_req.status_code == 200:
        return "ok 200."
    else:
        return "ERROR : " + str(twitter_req.status_code)