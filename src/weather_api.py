# OpenWeather API 사용
import json

from requests import get

from .secret_config import weather_api_key

def get_weather(city='Seoul'):
    URL = 'http://api.openweathermap.org/data/2.5/weather' + \
            f'?q={city}&appid={weather_api_key}&lang=kr'
    weather = {}
    res = get(URL)
    if res.status_code == 200:
        result = res.json()
        weather['main'] = result['weather'][0]['main']
        weather['description'] = result['weather'][0]['description']
        icon = result['weather'][0]['icon']
        weather['icon'] = f'http://openweathermap.org/img/w/{icon}.png'
        weather['etc'] = result['main']
    else:
        print('error', res.status_code)
    return weather

def inform_weather(kakao):
    weather = get_weather()
    # print(json.dumps(weather, indent=4, ensure_ascii=False)) # utf8 사용
    description = weather['description']
    temp = weather['etc']['temp'] - 273.15
    humi = weather['etc']['humidity']

    info = f"현재 날씨는 {description}! 이고, \
            기온은 {temp:.1f}! 도, 습도는 {humi:.1f}퍼센트 입니다."
    kakao.synthesize(info)
