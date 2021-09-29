from kakao_api import KakaoSound, record
from weather_api import inform_weather
from msg_list import *

def open_door():
    print('문을 열었습니다.')

def close_door():
    print('문을 닫았습니다.')

def led_on():
    print('전등을 켰습니다.')

def led_off():
    print('전등을 껐습니다.')

def process(audio_data):
    kakao = KakaoSound()
    msg = kakao.recognize(audio_data)

    if msg in weather_msg_list:
        inform_weather(kakao)
    elif msg in door_open_msg_list:
        open_door()
    elif msg in door_close_msg_list:
        close_door()
    elif msg in led_on_msg_list:
        led_on()
    elif msg in led_off_msg_list:
        led_off()

# 버튼 누른 경우 - 일단 5초간 녹음
audio = record()
# 버튼 뗀 경우 - 녹음 종료, 음성 인식 처리 시작
try:
    process(audio)
except Exception as e:
    print('에러 발생:', e)
