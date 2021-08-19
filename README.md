# CSV File Upload to Database

## Description
A self-learning project (work in progress) written in ```Python``` which provides a simple button on the frontend to upload a CSV file, and then pushes it to the database.

## Tech Stack
* HTML to receive .CSV file using jinja2 template
* Pyramid as a web server
* SQLAlchemy to connect with the database
* SQLite as Database

## Steps followed (so far)
* Receive file via browse button
* Detect schema of .csv file (Currently INT, REAL and TEXT supported)
* Keep alphanumeric characters from filename
* Create table with a dynamic SQL query with this new sanitized name and correct schema type
* Insert into table using a SQL query

## How to run
Run the following command
```console
./python3 app.py
```

Visit http://localhost:6543/

## Future improvements
* Retrieve data from DB on the frontend
* Give an option to select from the tables uploaded so far
* Use PostgreSQL server
* Use Celery