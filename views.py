from numpy import result_type
from pyramid.response import Response
from pyramid.view import view_config
import pandas as pd
from dbutil import create_table, insert_into_table, pull_from_table
from util import detect_schema, sanitize_name

@view_config(route_name='home', renderer='csv_upload.jinja2')
def home_view(request):
    return dict()

@view_config(route_name='upload')
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
    return Response(df.to_html())

