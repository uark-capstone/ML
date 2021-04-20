#region Imports
import os
import io
import json
import datetime
from PIL import Image

from requests.models import Response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from aws import rekognition as rek
from aws import bucket as bucket

from utils import util as util
from utils import backendConnector as backend

from predict import predict as predict
#endregion

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

#region AWS
queue = []

def process_queue():
    global queue

    cleaned_queue = [q[1] for q in queue]

    tiled_image = util.concat(cleaned_queue)
    in_mem_file = io.BytesIO()
    tiled_image.save(in_mem_file, format='png')
    in_mem_file.seek(0)

    saved_file_name = bucket.upload_to_bucket(in_mem_file)

    if (saved_file_name):
        results, emotion_arrays = process_and_get_emotion_arrays(saved_file_name)
        bucket.delete_from_bucket(saved_file_name)

        file_path = './prediction_data/user-ryan.json'

        input_data, output_data = predict.load_data(file_path)
        model = predict.train_model(input_data, output_data)

        for i, emotion_array in enumerate(emotion_arrays):
            data_to_test = []
            data_to_test.append(emotion_array)

            prediction = model.predict(data_to_test)
            print(prediction)        

            emotion_entry = queue[i][0]

            values = ["Not listening", "Neutral", "Actively Listening"]

            emotion_entry['emotions'] = values[int(prediction[0])]
            emotion_entry['percent'] = 100

            backend.addEmotion(emotion_entry)

        queue = []
    else:
        results = json.dumps({'error': 'failed to upload/process file'})       

    return results


class RekognitionQueue(Resource):
    def post(self):
        global queue
        json_data = request.get_json(force=True)
        user_id = json_data['userId']
        lecture_id = json_data['lectureId']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        base_64_string = json_data['base64String']

        # see base64.txt for working encoding
        image = util.stringToImage(bytes(base_64_string, 'utf-8'))
        image = Image.open(image)

        user_data = {
            'lecture_id': lecture_id,
            'user_id': user_id,
            'timestamp': timestamp
        }

        if len(queue) < 8:
            queue.append((user_data, image))
            return json.dumps({'success': 'Added item to queue {}'.format(len(queue))})    
        elif len(queue) == 8:
            queue.append((user_data, image))
            return process_queue()
        else:
            queue = []
            return json.dumps({'error': 'queue bigger than 9'})    



api.add_resource(RekognitionQueue, '/rekognition-queue')


class Rekognition(Resource):
    def get(self, photo_name):
        result = rek.detect_faces(photo_name)
        return result


api.add_resource(Rekognition, '/rekognition', '/rekognition/<string:photo_name>')
#endregion

#region Data Prediction Training
class PredictionTraining(Resource):
    @cross_origin()
    def post(self):
        json_data = request.get_json(force=True)
        user_id = json_data['userId']
        output_value = json_data['outputValue'] # 0 = not paying attention; 1 = neutral; 2 = actively listening
        base_64_string = json_data['base64String']

        if output_value not in [0, 1, 2]:
            return json.dumps({'error': 'Invalid output value'}) 
        else:
            result, emotion_values = process_and_get_emotion_array(base_64_string)

            if (result != None):
                file_path = './prediction_data/user-' + user_id + '.json'

                try:
                    with open(file_path, 'r') as prev_data:
                        data = json.load(prev_data) 
                        prev_data.close()
                except:
                    data = {
                        'input_data': [],
                        'output_data': []
                    }

                with open(file_path, 'w') as prediciton_file:
                    data['input_data'].append(emotion_values)
                    data['output_data'].append(output_value)

                    json.dump(data, prediciton_file)
                    prediciton_file.close()

                result = json.dumps(result)
            else:
                result = json.dumps({'error': 'failed to upload/process file'})    
        return result

api.add_resource(PredictionTraining, '/predict/training')
#endregion


#region Data Prediction 
class Prediction(Resource):
    @cross_origin()
    def post(self):
        json_data = request.get_json(force=True)
        user_id = json_data['userId']
        base_64_string = json_data['base64String']

        file_path = './prediction_data/user-' + user_id + '.json'

        result, emotion_values = process_and_get_emotion_array(base_64_string)

        data_to_test = []
        data_to_test.append(emotion_values)

        prediction_result = predict.train_and_predict(file_path, data_to_test)
        print(prediction_result)

        return json.dumps({'result': str(prediction_result[0])})

api.add_resource(Prediction, '/predict')
#endregion


#region Misc
class Ping(Resource):
    def get(self):
        return backend.BACKEND_URL

api.add_resource(Ping, '/ping')
#endregion


#region Helper Functions
def process_and_get_emotion_array(base_64_string):
    image = util.stringToImage(bytes(base_64_string, 'utf-8'))
    saved_file_name = bucket.upload_to_bucket(image)

    if (saved_file_name):
        result = rek.detect_faces(saved_file_name)

        emotions = result[0]['Emotions']
        sorted_emotions = sorted(emotions, key=lambda x: x['Type'])

        proper_order = ['ANGRY', 'CALM', 'CONFUSED', 'DISGUSTED', 'FEAR', 'HAPPY', 'SAD', 'SURPRISED']

        emotion_values = []
        for i, emotion in enumerate(sorted_emotions):
            if emotion['Type'] == proper_order[i]:
                emotion_values.append(emotion['Confidence'])

        bucket.delete_from_bucket(saved_file_name)

        return result, emotion_values

    return None, None

def process_and_get_emotion_arrays(saved_file_name):
    results = rek.detect_faces(saved_file_name)
    emotion_values = []

    for i, result in enumerate(results):
        emotions = result['Emotions']
        sorted_emotions = sorted(emotions, key=lambda x: x['Type'])

        proper_order = ['ANGRY', 'CALM', 'CONFUSED', 'DISGUSTED', 'FEAR', 'HAPPY', 'SAD', 'SURPRISED']

        local_emotion_values = []
        for i, emotion in enumerate(sorted_emotions):
            if emotion['Type'] == proper_order[i]:
                local_emotion_values.append(emotion['Confidence'])

        emotion_values.append(local_emotion_values)
        
    return results, emotion_values
#endregion


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
