--Query type: DQL
WITH temp_result AS (
    SELECT 'ñn' AS col1, 'n' AS col2
    UNION ALL
    SELECT 'ñn' AS col1, 'n' AS col2
)
SELECT
    CASE
        WHEN col1 COLLATE Latin1_General_CI_AS LIKE '%' + col2 COLLATE Latin1_General_CI_AS + '%' THEN 1
        ELSE 0
    END AS [contains]
FROM temp_result;

WITH temp_result AS (
    SELECT 'ñn' AS col1
)
SELECT
    CASE
        WHEN col1 COLLATE Latin1_General_CI_AS LIKE '%' + 'n' COLLATE Latin1_General_CI_AS + '%' THEN 1
        ELSE 0
    END AS [contains]
FROM temp_result;