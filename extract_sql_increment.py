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
    """Handles connection to AWS Redshift cluster"""
    try:
        # connect to the RS dwh cluster
        conn = psycopg2.connect(
            host=hostname,
            dbname=dbname,
            user=username,
            password=password,
            port=port
        )

        if conn is None:
            print('Connection failed')
            sys.exit(1)
        print(f"Connected to {hostname} successfully!")
        return conn
    except Exception as e:
        print(f"Connection failed, details of the error: {e}")
        return None
    
def execute_query(conn, query, fetch_mode=None):
    """Executes the query and returns the result
    Args:
        conn: connection object
        query: query to be executed
        fetch_mode: None, 'one', 'all'
    Returns:
        result: result of the query. None if fetch_mode is None, or one row if fetch_mode is 'one',
          or all if fetch_mode is 'all'"""
    # execute query
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            # fetch results (if asked)
            if fetch_mode == 'one':
              result = cursor.fetchone()
            elif fetch_mode == 'all':
              result = cursor.fetchall()
            else:
              result = None
            conn.commit()
            print(f'Query {query} executed successfully')
            return result
    except Exception as e:
        print(f"Error during extraction: {e}")
        sys.exit(1)


def create_table_animes(conn):
    """ Creates the table if it doesn't exist already
    Args:
        conn: connection object
    Returns:
        None
    """
    
    ddl_query = """
                CREATE TABLE IF NOT EXISTS animes (
                anime_id INT,
                name VARCHAR(300),
                genre VARCHAR(300),
                type VARCHAR(300),
                episodes INT,
                rating DOUBLE PRECISION,
                members INT,
                last_updated TIMESTAMP
                );
                """
    res = execute_query(conn, ddl_query, None)
    if res is None:
        print('Table animes created successfully/already exists')
        return
    else:
        print(f"Error in creating/connecting to the table animes")
    
def get_latest_updated_rs(conn):
    """Returns the latest updated date in the RS cluster"""
    # define query
    query = """SELECT COALESCE(MAX(last_updated), '1900-01-01') 
            FROM animes;"""
    # fetch result
    res = execute_query(conn, query, 'one')
    return res


def main():
    # execute connection and terminate if it fails
    conn = connect_to_aws_redshift()

    create_table_animes(conn)

    latest_update_rs = get_latest_updated_rs(conn)

    if latest_update_rs is not None:
        print(f"Last update: {latest_update_rs}")
    else:
        print("Failed to get last update")

    # close connection
    conn.close()

if __name__ == "__main__":
    main()