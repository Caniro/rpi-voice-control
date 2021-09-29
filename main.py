from signal import pause
from threading import Thread

from gpiozero import LED, Button
# import sounddevice as sd

from src.kakao_api import KakaoSound, VoiceRecorder
from src.weather_api import inform_weather
from src.msg_list import *
from src.servo_door import ServoDoor

btn = Button(14)
led = LED(15)
door = ServoDoor(18)
recorder = VoiceRecorder()

def process(audio_data):
    audio_data.seek(0)
    kakao = KakaoSound()
    msg = kakao.recognize(audio_data)

    if msg in weather_msg_list:
        inform_weather(kakao)
    elif msg in door_open_msg_list:
        door.open()
    elif msg in door_close_msg_list:
        door.close()
    elif msg in led_on_msg_list:
        led.on()
    elif msg in led_off_msg_list:
        led.off()
    elif msg in led_toggle_msg_list:
        led.toggle()
    elif msg in exit_msg_list:
        exit()

def button_pressed():
    global t

    # t = Thread(target=recorder.start_recording, kwargs={ 'device':device })
    t = Thread(target=recorder.start_recording)
    t.start()

def button_released():
    global t

    if t == None:
        return

    recorder.stop_recording()
    t.join()
    t = None
    try:
        process(recorder.get_record_data())
    except Exception as e:
        print('에러 :', e)

t = None
btn.when_pressed = button_pressed
btn.when_released = button_released

# 마이크 고를 수 있게 하고 싶은데 계속 에러 발생
# device_list = sd.query_devices()
# print(device_list)
# try:
#     idx = int(input('\nSelect microphone\'s number (press return for default): '))
#     device = device_list[idx].get('name')
#     print(device)
# except ValueError:
#     device = None

print('Ready to start!')
pause()
