-- tsql sql:
CREATE TABLE et3 ( date_part date, timestamp bigint, col2 varchar(50) );
WITH temp_result AS (
    SELECT '2022/01/01' AS date_part, 1643723400 AS timestamp, 'value1' AS col2
    UNION ALL
    SELECT '2022/01/02', 1643819800, 'value2'
),
     temp_result2 AS (
    SELECT '2022/01/03' AS date_part, 1643916200 AS timestamp, 'value3' AS col2
    UNION ALL
    SELECT '2022/01/04', 1644012600, 'value4'
)
INSERT INTO et3 (date_part, timestamp, col2)
SELECT CONVERT(date, date_part, 103) AS date_part, timestamp, col2
FROM (
    SELECT date_part, timestamp, col2
    FROM temp_result
    UNION ALL
    SELECT date_part, timestamp, col2
    FROM temp_result2
) AS CombinedResults;
SELECT * FROM et3;
-- REMORPH CLEANUP: DROP TABLE et3;
