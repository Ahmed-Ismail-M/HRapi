## API Endpoints FOR
#### Employee
- Register POST username , password '/api/v1/register'
- Sign In  POST username, password '/api/v1/login'

#### Attendance
- Create [auth required] post'/att'
- Index [auth required, perm required] get'/atts'

## Data Shapes
#### Employees
Column | Type
--- | --- |
id | SERIAL       PRIMARY KEY
name | VARCHAR(100) UNIQUE NOT NULL

#### Attendance
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
emp_id |  BIGINT      NOT NULL  REFERENCES employees(id) ON DELETE CASCADE
check_in  |  TIMESTAMP
check_out  |  TIMESTAMP
day | DATE
