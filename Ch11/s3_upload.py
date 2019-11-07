import boto3 as aws
import os.path
from functools import partial
from glob import iglob

def upload_file(fp, bucket):
    _, file_name = os.path.split(fp)
    s3 = aws.client("s3",
        aws_access_key_id = "YOURACCESSKEYID",
        aws_secret_access_key = "YOURSECRETACCESSKEY"
    )
    response = s3.upload_file(fp, bucket, file_name)
    return file_name, response

if __name__ == "__main__":
    fs = iglob("/path/to/data/files/*")
    uploads = map(partial(upload_file, bucket="your-backet-name"), fs)
    for file_name, _ in uploads :
        print(file_name)
