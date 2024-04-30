import pymysql
import csv
import boto3
import configparser
import sys, os
import credentials

my_config = credentials.read_config('pipeline.conf', 'mysql_config',
                                    ['hostname', 'port', 'username', 'database', 'password'])

# database variables

hostname = my_config[0]
port = my_config[1]
username = my_config[2]
dbname = my_config[3]
password = credentials.decode_string(my_config[4]) # this one is b64

# connection to the db

conn = pymysql.connect(host=hostname,
                       user=username,
                       password=password,
                       db=dbname,
                       port=int(port))

if conn is None:
    print('Connection failed')
    sys.exit(1)
print(f"Connected to {hostname} successfully!")

