import datetime
import csv
import os
import random
from string import ascii_letters as letters, digits

engine = None
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
        if 'float' in variable_data_type:
            return 'REAL'
        elif 'int' in variable_data_type:
            return 'INT'
    except:
        return 'VARCHAR'

def read_csv_from_file(filename):
    decoded_file = filename.read().decode('utf-8')
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

def detect_schema(rows):
    field_types = []    
    row_size = len(rows)
    if row_size == 0:
        print("Empty CSV File")
        return None
    
    col_size = len(rows[0])
    for i in range(col_size):
        real_type = True
        int_type = True
        for j in range(row_size):
            type_returned = datatype(rows[j][i])
            int_type &= (type_returned == 'INT')
            real_type &= (type_returned == 'REAL')
            if not (int_type or real_type):
                break
            
        if int_type:
            field_types.append('INT')
        elif real_type:
            field_types.append('REAL')
        else:
            field_types.append('VARCHAR')

    return field_types

def sanitize_name(filename):
    new_name = str()
    filename = os.path.splitext(filename)[0]
    for char in filename:
        if char in digits or char in letters:
            new_name += char
    if len(new_name) == 0:
        new_name = ''.join(random.choice(letters) for i in range(6))
    return new_name
