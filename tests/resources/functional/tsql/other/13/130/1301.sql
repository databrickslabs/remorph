--Query type: DDL
WITH temp_result AS (
    SELECT 2 AS column_b
)
SELECT *
INTO #temp_table
FROM temp_result;

ALTER TABLE #temp_table
WITH NOCHECK
ADD CONSTRAINT temp_check
CHECK (column_b > 1);

DROP TABLE #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
