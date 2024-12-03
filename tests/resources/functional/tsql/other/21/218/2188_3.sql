--Query type: DDL
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'temp_table_2')
    DROP TABLE temp_table_2;

WITH temp_table_2 AS (
    SELECT 1 AS id, 'test' AS name
)
SELECT * FROM temp_table_2
