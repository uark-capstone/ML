import time
import boto3

BUCKET = 'capstone-21-bucket'

def upload_to_bucket(file, save_name=None):
    s3 = boto3.client('s3')

    # use provided save_name or unix timestamp
    save_name = (save_name, str(int(time.time())))[save_name is None]
    
    try:
        s3.upload_fileobj(file, BUCKET, save_name)
    except:
        return None;

    return save_name


# for physical local file
# def upload_to_bucket(file_name, save_name=None):
#     s3 = boto3.client('s3')

#     save_name = (save_name, file_name)[save_name is None]

#     with open(file_name, "rb") as file:
#         s3.upload_fileobj(file, BUCKET, save_name)
