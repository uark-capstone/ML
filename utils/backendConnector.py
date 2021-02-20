import requests

BACKEND_URL = 'http://127.0.0.1:8080/'


def addEmotion(emotion_entry):
    print(emotion_entry)
    url = BACKEND_URL + 'emotion/addEmotion'

    response = requests.post(url, json = emotion_entry)

    if response.status_code != 200:
        print('Failed to add emotion to DB')
