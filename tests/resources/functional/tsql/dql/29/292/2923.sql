-- tsql sql:
WITH temp_result AS (SELECT 'customer' AS name, 'customer.tbl' AS physical_name, 1 AS database_id UNION ALL SELECT 'orders' AS name, 'orders.tbl' AS physical_name, 2 AS database_id) SELECT name, physical_name FROM temp_result WHERE database_id = DB_ID(N'customer');
