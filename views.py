from pyramid.response import Response
from pyramid.view import view_config
import pandas as pd
import json
from util.dbutil import create_table, insert_into_table, pull_from_table, retrieve_tables_from_db
from util.csvutil import detect_schema, sanitize_name

@view_config(route_name='home', renderer='templates/csv_upload.jinja2')
def home_view(request):
    return dict()

@view_config(route_name='get_tables', renderer='json')
def get_tables_view(request):
    list_of_tables = retrieve_tables_from_db()
    context = {'tables': list_of_tables}
    return context

@view_config(route_name='get_headers', renderer='json')
def get_headers_view(request):
    table_name = request.matchdict['table_name']
    

@view_config(route_name='upload', renderer='templates/display.jinja2')
def upload_view(request):
    filename = request.POST['csv_file'].filename
    input_file = request.POST['csv_file'].file
    headers, schema, rows  = detect_schema(input_file)
    if rows == 0:
        return Response('Empty CSV')

    table_name = sanitize_name(filename)
    create_table(table_name, headers, schema)
    insert_into_table(table_name, len(headers), rows)
    ResultSet = pull_from_table(table_name)
    df = pd.DataFrame(ResultSet, columns=headers)
    json_data = df.to_json(orient='records')
    table_json = dict()
    table_json['table_name'] = filename
    table_json['headers'] = headers
    table_json['data'] = json.loads(json_data)
    return table_json

