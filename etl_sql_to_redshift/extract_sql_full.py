import pymysql
import csv
import boto3
import configparser
import sys, os, logging
import credentials
import yaml

my_config = credentials.read_config('pipeline.conf', 'mysql_config',
                                    ['hostname', 'port', 'username', 'database', 'password'])

# database variables

hostname = my_config[0]
port = int(my_config[1])
username = my_config[2]
dbname = my_config[3]
password = credentials.decode_string(my_config[4]) # this one is b64

# connection to the db

conn = pymysql.connect(host=hostname,
                       user=username,
                       password=password,
                       db=dbname,
                       port=port)

if conn is None:
    logging.error('Connection failed')
    sys.exit(1)
logging.info(f"Connected to {hostname} successfully!")

# extract data
query_file = 'queries.yml'
try:
    with open(query_file, 'r') as qf:
        query_data = yaml.safe_load(qf)
        query = query_data['queries']['extract_anime']
    logging.info('Successfully read queries file.')
except Exception as e:
    logging.error(f"Error reading the query file, details: {e}")
    sys.exit(1)

# csv file location
local_filename = 'data/animes_extract.csv'

try:
    with conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
except Exception as e:
    logging.error(f"Error during extraction: {e}")
    sys.exit(1)

# write to csv
try:
    with open(local_filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(results)
        
    logging.info('Saved data to local CSV file successfully!')
except Exception as e:
    logging.error(f"Error during saving local file: {e}")
    sys.exit(1)

