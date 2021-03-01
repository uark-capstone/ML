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


def delete_from_bucket(file_name):
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=BUCKET, Key=file_name)
    except:
        return None
    
    return True

