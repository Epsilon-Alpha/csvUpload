from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import logging
import os

from configparser import ConfigParser

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    global DB_TYPE, DB_NAME, DB_HOST, DB_USER, DB_PASS, DB_STRING
    DB_TYPE = config.get('database', 'db_type')
    DB_NAME = config.get('database', 'db_name')
    if DB_TYPE == 'postgres':
        DB_HOST = config.get('postgres', 'host')
        DB_USER = config.get('postgres', 'user')
        DB_PASS = config.get('postgres', 'password')
        DB_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    else:
        DB_STRING = f'sqlite:///{DB_NAME}'

def db_connect():
    try:
        global engine
        read_config()
        engine = create_engine(DB_STRING)
        log.info("Connected to DB!")
        return True
    except SQLAlchemyError as e:
        log.error("Error while connecting to Database")
        return False

def get_database_type():
    return DB_TYPE

def create_table(table_name, headers, schema):
    cols, schema_len = len(headers), len(schema)
    if cols == 0:
        log.error("No column in file!")
    elif cols != schema_len:
        log.error("Data inconsistency.")

    if engine == None:
        log.error("Database connectivity issue.")
    else:
        with engine.connect() as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_name};")
            sql = 'CREATE TABLE {} ('.format(table_name);

            temp = str()
            if DB_TYPE == 'postgres':
                for header, schema in zip(headers, schema):
                    temp += f'"{header}" {schema},'
            else:
                for header, schema in zip(headers, schema):
                    temp += f'`{header}` {schema},'

            sql += temp[:-1] + ");"
            conn.execute(sql)
    log.info(f"Table {table_name} created successfully!")

def insert_into_table(table_name, headers, rows):
    placeholders = ','.join('?' * len(headers))
    query = f'INSERT INTO {table_name} VALUES({placeholders})'
    with engine.connect() as conn:
        conn.execute(query, rows)
    log.info(f"Inserted into table {table_name} successfully!")
   
def insert_into_table_postgres_slow(table_name, headers, rows):
    for row in rows:
        headers_formatted = ','.join(f'"{h}"' for h in headers)
        row_formatted = str()
        for item in row:
            if "'" in item:
                item = item.replace("'", "''")
            row_formatted += f"E'{item}',"
        row_formatted = row_formatted[:-1]
        query = f'INSERT INTO {table_name} ({headers_formatted}) VALUES({row_formatted})'
        with engine.connect() as conn:
           conn.execute(query)
    log.info(f"Inserted into table {table_name} successfully!")

def insert_into_table_postgres_efficient(table_name):
    CONNECTION_STRING = "host={} dbname={} user={} password={}".format(DB_HOST, DB_NAME, DB_USER, DB_PASS)
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    with open('temp.csv') as f:
        next(f)
        cur.copy_from(f, table_name.lower(), sep=',')
        conn.commit()
        conn.close()
    os.remove('temp.csv')

def pull_from_table(table_name):
    if DB_TYPE == 'postgres':
        table_name = table_name.lower()
    with engine.connect() as conn:
        metadata = MetaData()
        data = Table(table_name,metadata,autoload=True,autoload_with=engine)
        query = select([data])
        ResultProxy = conn.execute(query)
        ResultSet = ResultProxy.fetchall()
    
    log.info(f"Data pulled from table {table_name} successfully!")
    return ResultSet

def retrieve_tables_from_db():
    return engine.table_names()

def retrieve_columns_from_table(table_name):
    meta = MetaData()
    table = Table(table_name, meta, autoload_with=engine)
    return [col.name for col in table.columns]