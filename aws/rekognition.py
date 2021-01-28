import boto3
import json

BUCKET = 'capstone-21-bucket'

def detect_faces(photo):
    client=boto3.client('rekognition')
    response = client.detect_faces(Image={'S3Object':{'Bucket':BUCKET,'Name':photo}},Attributes=['ALL'])

    json_result = []

    for faceDetail in response['FaceDetails']:
        json_result.append(faceDetail)

    return json_result
