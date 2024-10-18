--Query type: DQL
WITH temp_result AS (SELECT 'sys.sp_columns' AS object_name)
SELECT OBJECT_DEFINITION(OBJECT_ID(object_name)) AS [Object Definition]
FROM temp_result;