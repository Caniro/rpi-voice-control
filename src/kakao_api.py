# 카카오 음성 인식 / 합성 API 사용
import sys
import os
import json
from io import BytesIO
from queue import Queue
from threading import Thread

from requests import post
from pydub import AudioSegment, playback
import sounddevice as sd
import soundfile as sf

from .secret_config import kakao_rest_api_key
from .color import MyColor

class VoiceRecorder:
    def __init__(self):
        self.recMem = None
        # self.recMem = BytesIO()
        self.q = Queue()
        self.continue_flag = True
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.sound = AudioSegment.from_wav(current_dir + 
                            '/../sound/notification.wav')

    def push_audio_queue(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    # def start_recording(self, fs=16000, channels=1, device=None):
    def start_recording(self, fs=16000, channels=1):
        sd.default.samplerate = fs
        sd.default.channels = channels
        # if device:
        #     sd.default.device = [device, None]
        self.recMem = BytesIO()

        try:
            with sf.SoundFile(self.recMem, mode='w', format='wav',
                    samplerate=fs, channels=channels) as file:
                with sd.InputStream(callback=self.push_audio_queue):
                    print('#' * 80)
                    print('Recording...\nrelease button to stop the recording')
                    self.notify()
                    self.continue_flag = True
                    while self.continue_flag:
                        # print('recording...')
                        file.write(self.q.get())
        except Exception as e:
            print('에러 :', e)

    def stop_recording(self):
        self.continue_flag = False
        print('#' * 80)
        print(f'Recording finished: {self.recMem.tell()}')
        self.notify()

    def get_record_data(self):
        return self.recMem

    def notify(self):
        t = Thread(target=lambda : playback.play(self.sound))
        t.start()

class KakaoSound:
    def __init__(self):
        self.kakao_recognize_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
        self.kakao_synthesize_url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
        self.headers = {
            "Authorization": "KakaoAK " + kakao_rest_api_key,
        }

    def recognize(self, audio_data):
        headers = {
            "Content-Type": "application/octet-stream",
            "X-DSS-Service": "DICTATION",
            **self.headers,
        }
        try:
            res = post(self.kakao_recognize_url, \
                    headers=headers, data=audio_data)
            result_json_string = res.text[ # 슬라이싱
                res.text.index('{"type":"finalResult"') : \
                res.text.rindex('}') + 1
            ]
            result = json.loads(result_json_string)
            value = result['value']
            print(f"\n음성 인식 결과> {MyColor.BOLD} {value} {MyColor.END}")
        except:
            value = None
            print("음성 인식 실패")
        return value

    def synthesize(self, msg):
        headers = {
            "Content-Type" : "application/xml",
            **self.headers,
        }
        data = f"""
        <speak>{msg}</speak>
        """.encode('utf-8')

        res = post(self.kakao_synthesize_url, headers=headers, data=data)
        if (res.status_code != 200):
            print(res, res.text)
        else:
            sound = BytesIO(res.content)
            song = AudioSegment.from_mp3(sound)
            playback.play(song)
