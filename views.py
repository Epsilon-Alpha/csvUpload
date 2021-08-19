from numpy import result_type
from pyramid.response import Response
from pyramid.view import view_config
from dbutil import insert_df_to_table
from util import create_dataframe, sanitize_name

@view_config(route_name='home', renderer='csv_upload.jinja2')
def home_view(request):
    return dict()

@view_config(route_name='upload')
def upload_view(request):
    filename = request.POST['csv_file'].filename
    input_file = request.POST['csv_file'].file
    df = create_dataframe(input_file)
    table_name = sanitize_name(filename)
    insert_df_to_table(table_name, df)
    return Response(df.to_html())

    # headers, schema, rows  = detect_schema_manual(input_file)
    # create_table(table_name, headers, schema)
    # insert_into_table(table_name, len(headers), rows)
    # ResultSet = pull_from_table(table_name)
    # df = pd.DataFrame(ResultSet, columns=headers)
    # return Response(df.to_html())

