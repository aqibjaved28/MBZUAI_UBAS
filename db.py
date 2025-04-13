import psycopg2

PG_CONN_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mbzuai_usertrack",
    "user": "postgres",
    "password": "123321"
}

def get_db_connection():
    return psycopg2.connect(**PG_CONN_PARAMS)
