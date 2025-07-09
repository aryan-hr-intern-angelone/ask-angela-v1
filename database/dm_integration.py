from psycopg_pool import ConnectionPool
import psycopg._encodings as _encodings
from config.env import env

_encodings.py_codecs[b'UNICODE'] = 'utf-8'

_pool_instance = None

connection_str = f"postgres://{env.aws.RDS_USERNAME}:{env.aws.RDS_PASSWORD}@{env.aws.RDS_CONNECTION_URI}:{env.aws.RDS_PORT}/{env.aws.RDS_DATABASE_NAME}"

def get_connection_pool():
    global _pool_instance
    if _pool_instance is None:
        _pool_instance = ConnectionPool(
            conninfo=connection_str,
            max_size=10,
            min_size=2,
            max_waiting=5,
            max_lifetime=300, 
            timeout=10,   
        )
    return _pool_instance

