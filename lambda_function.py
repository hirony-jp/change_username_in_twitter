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
    weather_url = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    weather_url = weather_url.format(city = city_name, key = weather_key)
    twitter_url = "https://api.twitter.com/1.1/account/update_profile.json"
    now = dt.datetime.now()
    jst = now + dt.timedelta(hours=9)
    jst = jst.hour

    # 天気データを取得
    weather_req = requests.get(weather_url)
    weather_data = json.loads(weather_req.text)
    weather_id = weather_data["weather"][0]["id"]

    # weather id をもとに分類
    if weather_id == 800:
        username = "ひろにぃ☀快晴"
        if jst >= 18 and jst <= 23 or jst >= 0 and jst <= 5:
            username = "ひろにぃ🌕快晴"
    elif weather_id >= 801:
        username = "ひろにぃ☀☁晴れ"
        if jst >= 18 and jst <= 23 or jst >= 0 and jst <= 5:
            username = "ひろにぃ🌕☁晴れ"
    elif weather_id >= 802 and weather_id <= 804:
        username = "ひろにぃ☁くもり"
    elif weather_id >= 300 and weather_id <= 321:
        username = "ひろにぃ🌂霧雨"
    elif weather_id >= 500 and weather_id <= 531:
        username = "ひろにぃ☔あめ"
    elif weather_id >= 200 and weather_id <= 232:
        username = "ひろにぃ⚡☔雷雨"
    elif weather_id >= 600 and weather_id <= 622:
        username = "ひろにぃ⛄ゆき"
    elif weather_id >= 900:
        username = "ひろにぃ🌀やっべぇ"

    # set username parameter.
    params = { "name" : username }

    # update Twitter username.
    twitter_req = twitter.post(twitter_url, params = params)

    if twitter_req.status_code == 200:
        return "ok 200."
    else:
        return "ERROR: " + str(twitter_req.status_code)