from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import logging

from sqlalchemy.sql.expression import table

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DB_TYPE = None

def db_connect(db_string):
    try:
        global engine
        global DB_TYPE
        if 'postgres' in db_string:
            DB_TYPE = 'postgres'
        elif 'sqlite in db_string':
            DB_TYPE = 'sqlite'

        engine = create_engine(db_string)
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
   
# def insert_into_table_postgres(table_name, headers, rows):
#     for row in rows:
#         headers_formatted = ','.join(f'"{h}"' for h in headers)
#         row_formatted = str()
#         for item in row:
#             if "'" in item:
#                 item = item.replace("'", "''")
#             row_formatted += f"E'{item}',"
#         row_formatted = row_formatted[:-1]
#         query = f'INSERT INTO {table_name} ({headers_formatted}) VALUES({row_formatted})'
#         with engine.connect() as conn:
#            conn.execute(query)
#     log.info(f"Inserted into table {table_name} successfully!")

def postgres_insert(table_name):
    conn = psycopg2.connect("host=localhost dbname=testdb user=postgres password=00000000")
    cur = conn.cursor()
    with open('temp.csv') as f:
        next(f)
        cur.copy_from(f, table_name.lower(), sep=',')
        conn.commit()
        conn.close()

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