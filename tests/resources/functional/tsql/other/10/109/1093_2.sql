-- tsql sql:
WITH customers AS ( SELECT 1 AS customer_id, 25 AS age UNION ALL SELECT 2, 30 UNION ALL SELECT 3, 35 UNION ALL SELECT 4, 40 ) SELECT CASE WHEN SUM( CASE WHEN age > 18 THEN 1 ELSE 0 END ) > 1 THEN 'Majority are adults' ELSE 'Majority are minors' END AS result FROM customers;
