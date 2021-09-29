# 카카오 음성 인식 / 합성 API 사용
import json
from requests import post
from io import BytesIO
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment, playback
from secret_config import kakao_rest_api_key

def record(seconds=5, fs=16000, channels=1):
    data = sd.rec(int(seconds * fs), samplerate=fs, channels=channels)
    sd.wait()
    audio = BytesIO()
    sf.write(audio, data, fs, format="wav") # format 필수
    audio.seek(0)
    return audio

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
            res = post(self.kakao_recognize_url, headers=headers, data=audio_data)
            result_json_string = res.text[ # 슬라이싱
                res.text.index('{"type":"finalResult"'):res.text.rindex('}') + 1
            ]
            result = json.loads(result_json_string)
            value = result['value']
            print(f"음성 인식 결과> {value}\n")
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
