-- tsql sql:
CREATE TABLE orders (
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus VARCHAR(50)
);

CREATE TABLE customers (
    c_custkey INT,
    c_name VARCHAR(100),
    c_address VARCHAR(200)
);

INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus)
VALUES (4, 4, 'DEFAULT');

INSERT INTO customers (c_custkey, c_name, c_address)
VALUES (4, 'Customer 4', 'Address 4');

WITH src AS (
    SELECT 1 AS o_orderkey, 1 AS o_custkey, 'Customer 1' AS c_name
    UNION ALL
    SELECT 2, 2, 'Customer 2'
    UNION ALL
    SELECT 3, 3, 'Customer 3'
)
SELECT o_orderkey, o_custkey, c_name
FROM src;

SELECT *
FROM orders;

SELECT *
FROM customers;
