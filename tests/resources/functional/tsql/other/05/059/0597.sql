--Query type: DDL
WITH cte_indexes AS (
    SELECT *
    FROM sys.indexes
)
SELECT *
FROM cte_indexes;
