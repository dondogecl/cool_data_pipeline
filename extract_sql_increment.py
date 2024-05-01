import csv
import boto3
import psycopg2
import pymysql
import sys, os, logging
import credentials

my_config = credentials.read_config('pipeline.conf', 'aws_creds',
                                    ['database', 'username', 'hostname',
                                      'port', 'access_key', 'secret_key', 'region',
                                      'password'])

# database variables

dbname = my_config[0]
username = my_config[1]
hostname = my_config[2]
port = int(my_config[3])
access_key, secret_key = credentials.decode_credentials(my_config[4], my_config[5])
region = my_config[6]
password = credentials.decode_string(my_config[7])

# Create a RedShift Client
client = boto3.client(
    'redshift-serverless',
    region_name=region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)


def connect_to_aws_redshift():

    try:
        # connect to the RS dwh cluster
        conn = psycopg2.connect(
            host=hostname,
            dbname=dbname,
            user=username,
            password=password,
            port=port
        )
        return conn
    except Exception as e:
        print(f"Connection failed, details of the error: {e}")
        return None
    
# execute connection and terminate if it fails
conn = connect_to_aws_redshift()

if conn is None:
    print('Connection failed')
    sys.exit(1)
print(f"Connected to {hostname} successfully!")


# define query
query = """SELECT COALESCE(MAX(LastUpdated), '1900-01-01') 
            FROM animes;"""
# execute query
try:
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        print(result[0])
except Exception as e:
    print(f"Error during extraction: {e}")
    sys.exit(1)

conn.commit()

# close connection
conn.close()




