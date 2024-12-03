--Query type: DQL
DECLARE @varname INT;
SET @varname = NULL;

WITH cte AS (
    SELECT 1 AS c_custkey
    UNION ALL
    SELECT NULL AS c_custkey
)
SELECT c_custkey
FROM cte
WHERE c_custkey = @varname OR c_custkey IS NULL;
