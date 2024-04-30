import pymysql
import csv
import boto3
import configparser
import sys, os, logging
import credentials

# aws variables
aws_s3_config = credentials.read_config('pipeline.conf', 'aws_boto_credentials', ['access_key', 'secret_key', 'bucket_name'])
access_key, secret_key = credentials.decode_credentials(aws_s3_config[0], aws_s3_config[1])
bucket_name = aws_s3_config[2]

# s3 upload
s3 = boto3.client('s3', 
                  aws_access_key_id=access_key, 
                  aws_secret_access_key=secret_key)

local_filename = 'data/animes_extract.csv'
s3_file = local_filename

try:
    s3.upload_file(local_filename, bucket_name, s3_file)
    print("Upload Successful")
except Exception as e:
    print(f"Upload Failed, details: {e}")