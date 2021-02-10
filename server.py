#region Imports
import os
import json
import werkzeug
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

from aws import rekognition as rek
from aws import bucket as bucket

from utils import util as util
#endregion

app = Flask(__name__)
api = Api(app)

#region AWS
class Rekognition(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        base_64_string = json_data['base64String']

        # see base64.txt for working encoding
        image = util.stringToImage(bytes(base_64_string, 'utf-8'))

        saved_file_name = bucket.upload_to_bucket(image)

        if (saved_file_name):
            result = rek.detect_faces(saved_file_name)
        else:
            result = json.dumps({'error': 'failed to upload/process file'})        

        return result

api.add_resource(Rekognition, '/rekognition')
#endregion

if __name__ == "__main__":
    app.run(debug=True)
