--Query type: DML
CREATE TABLE customers (c_custkey INT, c_name VARCHAR(50), c_address VARCHAR(100));
CREATE TABLE orders (o_orderkey INT, o_custkey INT, o_orderstatus VARCHAR(50));
WITH src AS (
    SELECT 1 AS n1, 'John' AS n2, 'New York' AS n3
    UNION ALL
    SELECT 2 AS n1, 'Jane' AS n2, 'London' AS n3
)
INSERT INTO customers (c_custkey, c_name, c_address)
SELECT n1, n2, n3
FROM src;
INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus)
SELECT n3, n2, 'DEFAULT'
FROM src;
SELECT *
FROM customers;
SELECT *
FROM orders;
-- REMORPH CLEANUP: DROP TABLE customers;
-- REMORPH CLEANUP: DROP TABLE orders;
