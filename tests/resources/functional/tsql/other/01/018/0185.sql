--Query type: DDL
SELECT *
INTO customers
FROM (
    VALUES (1, 'Customer#1'),
           (2, 'Customer#2')
) AS customer (custkey, name);

SELECT *
FROM customers;
-- REMORPH CLEANUP: DROP TABLE customers;