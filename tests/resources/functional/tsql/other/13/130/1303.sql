--Query type: DDL
SELECT *
INTO #temp_result
FROM (
    VALUES (1, 2),
           (3, 4)
) AS temp_table (col1, col2);

SELECT *
FROM #temp_result;

-- REMORPH CLEANUP: DROP TABLE #temp_result;