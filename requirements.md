## API Endpoints FOR
#### Employee
- Register POST username , password '/api/v1/register'
- Sign In  POST username, password '/api/v1/login'

#### Attendance
- Create [auth required] POST date, check in or out '/api/v1/attendance'
- Index by User [auth required] GET'/api/v1/attendances'
- Daily Index [auth required] GET'/api/v1/daily/attendances'
- Daily Report [auth required] GET'api/v1/report/attendances'
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
