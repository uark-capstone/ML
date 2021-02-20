import os
import json
import time
import requests

LIVE_URL = os.getenv('BACKEND_URL')
BACKEND_URL = ('http://0.0.0.0:8080/', LIVE_URL)[LIVE_URL != None]

print('Backend url: ' + BACKEND_URL)

def addEmotion(emotion_entry):
    url = BACKEND_URL + 'emotion/addEmotion'
    response = requests.post(url, json = emotion_entry)

    if response.status_code != 200:
        msg = '\033[93m' + '------------ERROR------------ \n' \
              '[' + time.ctime() + '] \n' + \
              'Failed to add emotion to DB; Response: ' + str(response) + '\n' \
              'url: ' + url + '\n' \
              'data: ' + '\n'  + json.dumps(emotion_entry, indent=2) + '\n' \
              '-----------------------------' + '\033[0m'

        print(msg)
    else:
        print('\033[92m' + '[' + time.ctime() +'] Added emotion to DB' + '\033[0m')