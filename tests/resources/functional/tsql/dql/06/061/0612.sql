--Query type: DQL
WITH temp_result AS (
    SELECT 'c_custkey' AS COLUMN_NAME, 'integer' AS DATA_TYPE, 1 AS ORDINAL_POSITION
    UNION ALL
    SELECT 'c_name', 'varchar(25)', 2
    UNION ALL
    SELECT 'c_address', 'varchar(40)', 3
)
SELECT COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION
FROM temp_result
ORDER BY ORDINAL_POSITION DESC;
