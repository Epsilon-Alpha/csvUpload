# CSV File Upload to Database

## Description
A self-learning project (work in progress) written in ```Python``` which provides a simple button on the frontend to upload a CSV file, and then pushes it to the database.

## Tech Stack
* HTML to receive .CSV file using jinja2 template
* Pyramid as a web server
* SQLAlchemy to connect with the database
* SQLite as Database
* jQuery + HTML + CSS template for file upload

## Steps followed (so far)
* Receive file via browse button
* Detect schema of .csv file (Currently INT, REAL and TEXT supported)
* Keep alphanumeric characters from filename
* Create table with a dynamic SQL query with this new sanitized name and correct schema type
* Insert into table using a SQL query
* Retrieve the table from database and send JSON to frontend
* Display table using [DataTables](https://datatables.net/)

## How to run
* Run the following command
```console
./python3 app.py
```

* Visit http://localhost:6543/
* Select a CSV file which is UTF-8 compatable, and has the first row as headers.

## Future improvements
* Add test cases
* Give an option to select from the tables uploaded so far
* Use PostgreSQL server
* Use Celery

## References
* [Process CSV file from web form with Python](https://stackoverflow.com/questions/22009034/how-to-process-uploaded-csv-file-from-web-form-with-python-3)
* [Validate Date Format](https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python)
* [Execute SQL with SQLAlchemy](https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/)
* [Insert CSV into database](https://python.plainenglish.io/comparison-of-methods-for-importing-bulk-csv-data-into-mysql-using-python-5890dbf57419)
* [Render Pandas Dataframe as HTML](https://www.geeksforgeeks.org/rendering-data-frame-to-html-template-in-table-view-using-django-framework/)
* [File upload templates](https://freshdesignweb.com/jquery-html5-file-upload/)
