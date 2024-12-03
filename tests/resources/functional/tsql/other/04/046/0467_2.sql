--Query type: DCL
DECLARE @var1 INT;
SET @var1 = 10;

WITH temp_result AS (
    SELECT 1 AS col1, 2 AS col2
    UNION ALL
    SELECT 3, 4
)
SELECT col1, col2
FROM temp_result
WHERE col1 = @var1
