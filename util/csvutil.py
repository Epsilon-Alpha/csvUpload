import datetime
import csv

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def validate_num(num_text):
    return num_text.replace('.','',1).isdigit()

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        return False
    return True

def datatype(entity):
    try:
        variable_data_type = str(type(eval(entity)))
        if validate_num(entity):
            if 'float' in variable_data_type:
                return 'REAL'
            elif 'int' in variable_data_type:
                return 'INT'
        else:
            return 'VARCHAR'
    except:
        return 'VARCHAR'

def read_csv_from_file_and_save(filename):
    read_file = filename.read()
    decoded_file = read_file.decode('utf-8')
    with open('temp.csv', 'w') as f:
        f.write(decoded_file)
    
    file_t = decoded_file.splitlines()
    csvreader = csv.reader(file_t)
    return csvreader

def detect_headers(csvreader):
    fields = next(csvreader)
    return fields

def get_rows_from_csv(csvreader):
    rows = []
    for row in csvreader:
        rows.append(row)
    return rows

