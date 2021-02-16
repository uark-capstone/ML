import requests

BACKEND_URL = 'localhost:8080/emotion/addEmotion'


def addEmotion(emotion_entry):
    print(emotion_entry)
    url = BACKEND_URL + 'emotion/addEmotion'
    # requests.post(url, data = emotion_entry)