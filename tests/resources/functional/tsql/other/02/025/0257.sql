--Query type: DDL
WITH temp_result AS (
    SELECT '2022/01/01' AS date_part, 1643723400 AS timestamp, 'value1' AS col2
    UNION ALL
    SELECT '2022/01/02', 1643819800, 'value2'
    UNION ALL
    SELECT '2022/01/03', 1643916200, 'value3'
    UNION ALL
    SELECT '2022/01/04', 1644012600, 'value4'
)
SELECT
    CONVERT(DATE, date_part, 103) AS date_part,
    timestamp,
    col2
FROM temp_result;
