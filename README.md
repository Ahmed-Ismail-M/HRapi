# AttendanceAPI Backend Project

## Getting Started

This repo contains a back-end app that manages employees attendance.
To get started run 'pip install -r requirements.txt' at src/



## Used Technologies
- SQLITE for the database
- Django for the application logic
- Django RestFrameWrok for rest api

## Steps to start the app

### 1.  DB Creation and Migrations
1. 'python manage.py migrate' will create database tables
2. 'python manage.py createsuperuser' to create admin user

### 2. Testing

"python manage.py test" will
1. Migrate test tables
2. run tests from test folder
3. Test models and routes
4. Drop test tables

### 3. Starting the server

- "'python manage.py runserver" will run the server on localhost/8000


