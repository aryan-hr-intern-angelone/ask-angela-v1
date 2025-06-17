import psycopg
from psycopg_pool import ConnectionPool
import psycopg._encodings as _encodings
from config.env import env

_encodings.py_codecs[b'UNICODE'] = 'utf-8'

_pool_instance = None

def get_connection_pool():
    global _pool_instance
    if _pool_instance is None:
        _pool_instance = ConnectionPool(
            conninfo=env.aws.DATAMART_HOST,
            max_size=10,
            min_size=2,
            max_waiting=5,
            max_lifetime=300, 
            timeout=10,   
        )
    return _pool_instance

