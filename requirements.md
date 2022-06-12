## API Endpoints FOR
#### Employees
- Index [auth required, perm required] get'/employees'
- Sign In  post'/signin'

#### Attendance
- Create [auth required] post'/att'
- Index [auth required, perm required] get'/atts'

## Data Shapes
#### Employees
Column | Type
--- | --- |
id | SERIAL       PRIMARY KEY
name | VARCHAR(100) UNIQUE NOT NULL
price | REAL         NOT NULL
category | VARCHAR(50)

#### Users
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
firstName |  VARCHAR(50) UNIQUE NOT NULL
lastName | VARCHAR(50)
password | VARCHAR     NOT NULL

#### Attendance
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
emp_id |  BIGINT      NOT NULL  REFERENCES employees(id) ON DELETE CASCADE
check_in  |  VARCHAR(20)
check_out  |  VARCHAR(20)
day | date
