## API Endpoints FOR
#### Employees
- Index [auth required, perm required] get'/employees'
- Sign In  post'/signin'

#### Attendance
- Create [auth required] post'/att'
- Index [auth required, perm required] get'/atts'

#### Orders
- Index get'/orders'
- Show get'/orders/:id'
- Create [token required] post'/orders'
- Delete [token required] delete'/orders'
- Update [token required] put'/orders/:id'

## Data Shapes
#### Products
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

#### Orders
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
user_id |  BIGINT      NOT NULL  REFERENCES users(id) ON DELETE CASCADE
status  |  VARCHAR(20)

#### OrdersProduct
Column | Type
--- | --- |
id | SERIAL  PRIMARY KEY
quantity | integer     NOT NULL
product_id |  bigint      NOT NULL REFERENCES products(id)       ON DELETE CASCADE
order_id |  bigint      NOT NULL REFERENCES orders(id)         ON DELETE CASCADE