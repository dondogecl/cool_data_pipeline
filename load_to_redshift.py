import boto3
import configparser
import psycopg2
import sys, os, logging
import credentials, aws_redshift



def main():
    # obtain credentials

    # if "pipeline.conf" exists in the current working directory:
    if os.path.exists('pipeline.conf'):
        logging.info('reading credentials from local environment')
        my_config = credentials.read_config('pipeline.conf', 'aws_creds',
                                            ['database', 'username', 'hostname',
                                            'port', 'access_key', 'secret_key', 
                                            'region', 'password', 'iam_role',
                                            ])
        my_boto_config = credentials.read_config('pipeline.conf', 'aws_boto_credentials',
                                                  ['account_id', 'bucket_name'])
                                                  
        # db variables
        database = my_config[0]
        username = my_config[1]
        hostname = my_config[2]
        port = int(my_config[3])
        access_key, secret_key = credentials.decode_credentials(my_config[4], my_config[5])
        region = my_config[6]
        password = credentials.decode_string(my_config[7])
        iam_role = my_config[8]
        # iam role
        account_id = credentials.decode_string(my_boto_config[0])
        bucket_name = my_boto_config[1]
    else:
        logging.info('reading credentials from environment variables')
        # read the variables from environment variables
        database = os.environ['DBNAME']
        username = os.environ['USERNAME']
        hostname = os.environ['HOSTNAME']
        port = int(os.environ['PORT'])
        access_key = os.environ['ACCESS_KEY']
        secret_key = os.environ['SECRET_KEY']
        region = os.environ['REGION']
        password = os.environ['PASSWORD']
        account_id = os.environ['IAM_ROLE']
        bucket_name = os.environ['BUCKET_NAME']


    # create boto client
    client = aws_redshift.boto_client(region=region, access_key=access_key, secret_key=secret_key)

    # create database connection
    conn = aws_redshift.connect_to_aws_redshift(hostname=hostname, dbname=database, 
                                        username=username, password=password, port=port)
    
    # COPY data from S3 to Redshift
    data_file = 'animes_increment.csv'
    object_path = f"s3://{bucket_name}/{data_file}"
    role_string = f"arn:aws:iam::{account_id}:role/{iam_role}"

    

    conn.close()

if __name__ == "__main__":
    main()