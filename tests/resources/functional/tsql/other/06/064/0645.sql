--Query type: DCL
WITH usa_customers AS ( SELECT 'John' AS name, 'USA' AS country, 25 AS age UNION ALL SELECT 'Alice', 'USA', 30 ) SELECT * FROM usa_customers;
