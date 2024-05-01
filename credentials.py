import base64
import os
import configparser

def encode_credentials(access_key: str, secret_key: str) -> tuple[str, str]:
    """Encode access_key and secret_key into base64 format"""
    encoded_access_key = base64.b64encode(access_key.encode('utf-8')).decode('utf-8')
    encoded_secret_key = base64.b64encode(secret_key.encode('utf-8')).decode('utf-8')
    return encoded_access_key, encoded_secret_key

def encode_string(plain_string: str) -> str:
    """Decode a given string from base64 format"""
    encoded_string = base64.b64encode(plain_string.encode('utf-8')).decode('utf-8')
    
    return encoded_string

def decode_credentials(access_key_64: str, secret_key_64: str) -> tuple[str, str]:
    """Decode access_key and secret_key from base64 format"""
    access_key = base64.b64decode(access_key_64).decode('utf-8')
    secret_key = base64.b64decode(secret_key_64).decode('utf-8')
    return access_key, secret_key

def decode_string(encoded_string: str) -> str:
    """Decode a given string from base64 format"""
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    
    return decoded_string

# read the value from pipeline.conf using configparser
def read_config(filename: str, section:str, keys: list) -> list[str]:
    """Read the value from a config file using configparser
    and returns the values as is"""
    config = configparser.ConfigParser(interpolation=None)
    # read the configuration file (if found)
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'Config file not found: {filename}') 

    config.read(filename)

    list_of_outputs = []
    
    for k in keys:
        try:
            value = config[section][k]
            list_of_outputs.append(value)
        except KeyError:
            raise KeyError(f'Key {k} not found in section {section}')
    
    return list_of_outputs

