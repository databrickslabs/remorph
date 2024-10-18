--Query type: DDL
CREATE TABLE customer (c_custkey INT, c_name VARCHAR(255), c_address VARCHAR(255));
CREATE TABLE orders (o_orderkey INT, o_custkey INT, o_orderstatus VARCHAR(255));
WITH customer_cte AS (
    SELECT c_custkey, c_name, c_address
    FROM customer
),
orders_cte AS (
    SELECT o_orderkey, o_custkey, o_orderstatus
    FROM orders
)
SELECT *
FROM customer_cte;
SELECT *
FROM orders_cte;
-- REMORPH CLEANUP: DROP TABLE customer;
-- REMORPH CLEANUP: DROP TABLE orders;