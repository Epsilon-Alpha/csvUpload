from pyramid.response import Response
from pyramid.view import view_config
import pandas as pd
import json
import os
import time

from sqlalchemy.exc import NoSuchTableError
from util.dbutil import get_database_type, create_table, insert_into_table, insert_into_table_postgres_efficient, insert_into_table_postgres_efficient, insert_into_table_postgres_slow, pull_from_table, retrieve_columns_from_table, retrieve_tables_from_db
from util.csvutil import detect_headers, read_csv_from_file_and_save, get_rows_from_csv
from util.tasks import detect_schema, sanitize_name

@view_config(route_name='home', renderer='templates/csv_upload.jinja2')
def home_view(request):
    return dict()

@view_config(route_name='get_tables', renderer='json')
def get_tables_view(request):
    list_of_tables = retrieve_tables_from_db()
    if len(list_of_tables) == 0:
        return Response('No tables found.', status_code=404)
        
    data = {'tables': list_of_tables}
    return data

@view_config(route_name='get_headers', renderer='json')
def get_headers_view(request):
    try:
        table_name = request.matchdict['table_name']
        list_of_columns = retrieve_columns_from_table(table_name)
        data = {'columns': list_of_columns}
        return data
    except NoSuchTableError:
        return Response('Table not found.', status_code=404)

@view_config(route_name='upload', renderer='templates/display.jinja2')
def upload_view(request):
    filename = request.POST['csv_file'].filename
    input_file = request.POST['csv_file'].file
    csvreader = read_csv_from_file_and_save(input_file)
    headers = detect_headers(csvreader)
    rows = get_rows_from_csv(csvreader)
    if rows == None:
        return Response('Empty CSV')

    schema  = detect_schema.delay(rows)
    table_name = sanitize_name.delay(filename)
    while not (schema.ready() and table_name.ready()):
        time.sleep(1)
    
    schema = schema.get()
    table_name = table_name.get()
    create_table(table_name, headers, schema)
    DB_TYPE = get_database_type()
    if DB_TYPE == 'sqlite':
        insert_into_table(table_name, headers, rows)
    else:
        try:
            insert_into_table_postgres_efficient(table_name)
        except:
            insert_into_table_postgres_slow(table_name, headers, rows)

    os.remove('temp.csv')
    ResultSet = pull_from_table(table_name)
    df = pd.DataFrame(ResultSet, columns=headers)
    json_data = df.to_json(orient='records')
    table_json = dict()
    table_json['table_name'] = filename
    table_json['headers'] = headers
    table_json['data'] = json.loads(json_data)
    return table_json

