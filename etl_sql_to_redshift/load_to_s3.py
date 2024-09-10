import csv
import boto3
import configparser
import sys, os, logging
import credentials

# aws variables
aws_s3_config = credentials.read_config('pipeline.conf', 'aws_boto_credentials', ['access_key', 'secret_key', 'bucket_name'])
access_key, secret_key = credentials.decode_credentials(aws_s3_config[0], aws_s3_config[1])
bucket_name = aws_s3_config[2]

def initialize_s3(access_key, secret_key):
    try:
        s3 = boto3.client('s3', 
                    aws_access_key_id=access_key, 
                    aws_secret_access_key=secret_key)
    except Exception as e:
        logging.error(f"Error during s3 initialization: {e}")
        sys.exit(1)
    return s3


class S3Client:
    def __init__(self, access_key, secret_key) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = self._initialize_s3_client()

    def _initialize_s3_client(self) -> boto3.client:
        return boto3.client(
            's3', aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key)

    def get_client(self) -> boto3.client:
        return self.client
    
    def upload_to_s3(self, local_filename, s3_filename, bucket_name) -> bool:
        """Uploads a file to an S3 bucket"""
        try:
            self.client.upload_file(local_filename, bucket_name, s3_filename)
            logging.info("Upload Successful")
            return True
        except Exception as e:
            logging.error(f"Upload Failed, details: {e}")
            return False


