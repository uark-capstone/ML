from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import os
import json
import werkzeug

from aws.rekognition import *
from aws.bucket import *

app = Flask(__name__)
api = Api(app)

# AWS
class Rekognition(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file = args['file']

        # Upload file to S3-Bucket & proccess with rekognition
        saved_file_name = upload_to_bucket(file)
        if (saved_file_name):
            result = detect_faces(saved_file_name)
        else:
            result = json.dumps({'error': 'failed to upload/process file'})

        return result

api.add_resource(Rekognition, '/rekognition')


if __name__ == "__main__":
    app.run(debug=True)