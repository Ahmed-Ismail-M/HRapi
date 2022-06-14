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


## API Endpoints
#### Employee
- Register POST username , password '/api/v1/register'
- Sign In  POST username, password '/api/v1/login'

#### Attendance
- Create [auth required] POST date, check in or out '/api/v1/attendance'
- Index by User [auth required] GET'/api/v1/attendances'
- Daily Index by User [auth required] GET'/api/v1/daily/attendances'
- Daily Report by User [auth required] GET'api/v1/report/attendances'
- All Attendances [auth required, permission required] GET'api/v1/allattendances'

## Data Shapes
#### Employees
Column | Type
--- | --- |
id | SERIAL       PRIMARY KEY
username | VARCHAR(100) UNIQUE NOT NULL

#### Attendance
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
emp_id |  BIGINT      NOT NULL  REFERENCES employees(id) ON DELETE CASCADE
check_in  |  TIMESTAMP
check_out  |  TIMESTAMP
date | DATE
is_attending | BOOL