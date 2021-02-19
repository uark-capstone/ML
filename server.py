#region Imports
import os
import json
import werkzeug
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

from aws import rekognition as rek
from aws import bucket as bucket

from utils import util as util
from utils import backendConnector as backend
#endregion

app = Flask(__name__)
api = Api(app)

#region AWS
class Rekognition(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        user_id = json_data['userId']
        lecture_id = json_data['lectureId']
        timestamp = json_data['timestamp']
        base_64_string = json_data['base64String']

        # see base64.txt for working encoding
        image = util.stringToImage(bytes(base_64_string, 'utf-8'))

        saved_file_name = bucket.upload_to_bucket(image)

        if (saved_file_name):
            result = rek.detect_faces(saved_file_name)

            emotions = result[0]['Emotions']
            for emotion in emotions:
                if emotion['Confidence'] > 1:
                    emotion_entry = {
                        'lecture_id': lecture_id,
                        'user_id': user_id,
                        'emotions': emotion['Type'],
                        'percent': emotion['Confidence']
                    }

                    backend.addEmotion(emotion_entry)

        else:
            result = json.dumps({'error': 'failed to upload/process file'})        

        return result

api.add_resource(Rekognition, '/rekognition-queue')
#endregion

if __name__ == "__main__":
    app.run(host='0.0.0.0')
