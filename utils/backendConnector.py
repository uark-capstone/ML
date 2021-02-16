import requests

BACKEND_URL = 'http://localhost:8080/'


def addEmotion(emotion_entry):
    print(emotion_entry)
    url = BACKEND_URL + 'emotion/addEmotion'

    respone = requests.post(url, json = emotion_entry)

    if respone.status_code != 200:
        print('Failed to add emotion to DB')
