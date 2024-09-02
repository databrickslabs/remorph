--Query type: DML
DECLARE @y1 INT = 30;
SET @y1 -= 3;
WITH temp_cte AS (
    SELECT 1 AS temp_column
)
SELECT @y1 AS Subtracted_3
FROM temp_cte;