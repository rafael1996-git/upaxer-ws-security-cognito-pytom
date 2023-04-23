import boto3
import json
import os


class Config:

    def __init__(self):
        self.client = boto3.client('s3')

    def get_config(self):
        bucket_name = os.environ['BUCKET_NAME']
        config_file = os.environ['CONFIG_FILE']
        return json.loads(self.client.get_object(Bucket=bucket_name, Key=config_file)['Body'].read().decode())
