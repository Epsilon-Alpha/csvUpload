import os
import random
from .csvutil import datatype
from string import ascii_letters as letters, digits
from celery import Celery

app = Celery('tasks', backend='rpc://', broker='pyamqp://localhost')

@app.task
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

@app.task
def sanitize_name(filename):
    new_name = str()
    filename = os.path.splitext(filename)[0]
    for char in filename:
        if char in digits or char in letters:
            new_name += char
    if len(new_name) == 0:
        new_name = ''.join(random.choice(letters) for i in range(6))
    return new_name
