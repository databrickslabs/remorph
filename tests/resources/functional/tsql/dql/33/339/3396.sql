--Query type: DQL
WITH temp_result AS ( SELECT 'customer' AS name, 'public' AS schema_name UNION ALL SELECT 'orders', 'public' ) SELECT name, schema_name AS SchemaName FROM temp_result WHERE schema_name = 'public' ORDER BY SchemaName;
