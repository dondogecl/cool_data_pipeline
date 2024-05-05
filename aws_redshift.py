import boto3
import configparser
import psycopg2
import sys
from typing import List, Optional, Tuple


def boto_client(region, access_key, secret_key):
    # Create a RedShift Client
    client = boto3.client(
        'redshift-serverless',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
)


def connect_to_aws_redshift(hostname, dbname, username, password, port) -> psycopg2.extensions.connection:
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

def execute_query(conn: psycopg2.extensions.connection, query: str, fetch_mode=None) -> Optional[List[Tuple]]:
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

def get_latest_updated_rs(conn) -> tuple:
    """Returns the latest updated date in the RS cluster"""
    # define query
    query = """SELECT COALESCE(MAX(last_updated), '1900-01-01') 
            FROM animes;"""
    # fetch result
    res = (execute_query(conn, query, 'one'),)
    return res

