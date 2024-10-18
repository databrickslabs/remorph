--Query type: DDL
CREATE TABLE #temp (c3 INT);
CREATE NONCLUSTERED INDEX idx_temp ON #temp (c3);
WITH cte AS (
    SELECT c3 = 1
)
SELECT *
FROM (
    VALUES (1)
) AS cte (c3);