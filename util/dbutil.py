from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def db_connect(db_name):
    try:
        global engine
        engine = create_engine(db_name)
        log.info("Connected to DB!")
    except SQLAlchemyError as e:
        err=str(e.__dic__['orig'])
        log.error("Error while connecting to SQLite", err)

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
            conn.execute("DROP TABLE IF EXISTS {};".format(table_name))
            sql = 'CREATE TABLE "{}" ('.format(table_name);

            temp =  str()
            for header, schema in zip(headers, schema):
                temp += f'`{header}` {schema},'

            sql += temp[:-1] + ");"
            conn.execute(sql)
        log.info(f"Table {table_name} created successfully!")

def insert_into_table(table_name, headers_len, rows):
    placeholders = ','.join('?' * headers_len)
    query = f'INSERT INTO {table_name} VALUES({placeholders})'
    with engine.connect() as conn:
        conn.execute(query, rows)
    log.info(f"Inserted into table {table_name} successfully!")

def pull_from_table(table_name):
    with engine.connect() as conn:
        metadata = MetaData()
        data = Table(table_name, metadata,autoload=True,autoload_with=engine)
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