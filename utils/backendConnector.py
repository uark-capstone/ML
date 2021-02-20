import os
import requests

LIVE_URL = os.getenv('BACKEND_URL')
BACKEND_URL = ('http://0.0.0.0:8080/', LIVE_URL)[LIVE_URL != None]

print('Backend url: ' + BACKEND_URL)

def addEmotion(emotion_entry):
    print(emotion_entry)
    url = BACKEND_URL + 'emotion/addEmotion'

    print(url)
    response = requests.post(url, json = emotion_entry)

    if response.status_code != 200:
        print(response)
        print('Failed to add emotion to DB')
