from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def db_connect():
    try:
        global engine
        engine = create_engine('sqlite:///testdb.db', echo = True)
        print("Connected to DB!")
    except SQLAlchemyError as e:
        err=str(e.__dic__['orig'])
        print("Error while connecting to SQLite", err)

def create_table(table_name, headers, schema):
    cols, schema_len = len(headers), len(schema)
    if cols == 0:
        print("No column in file!")
    elif cols != schema_len:
        print("Data inconsistency.")

    if engine == None:
        print("Database connectivity issue.")
    else:
        with engine.connect() as conn:
            conn.execute("DROP TABLE IF EXISTS {};".format(table_name))
            sql = 'CREATE TABLE "{}" ('.format(table_name);

            temp =  str()
            for header, schema in zip(headers, schema):
                temp += f'`{header}` {schema},'

            sql += temp[:-1] + ");"
            conn.execute(sql)

def insert_into_table(table_name, headers_len, rows):
    placeholders = ','.join('?' * headers_len)
    query = f'INSERT INTO {table_name} VALUES({placeholders})'
    with engine.connect() as conn:
        conn.execute(query, rows)

