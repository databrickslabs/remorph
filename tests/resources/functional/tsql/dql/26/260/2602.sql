-- tsql sql:
WITH temp_result AS (SELECT name FROM (VALUES ('customer1'), ('customer2')) AS customers (name)) SELECT FILE_IDEX((SELECT name FROM temp_result WHERE name = 'customer1')) AS 'Customer_ID';
