--Query type: DDL
WITH temp_table AS (SELECT 'value1' AS b1, 'value2' AS b2)
SELECT b2
FROM temp_table;
