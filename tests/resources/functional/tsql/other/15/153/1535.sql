--Query type: DML
DECLARE @d DECIMAL(7, 2) = 85.455;
DECLARE @f FLOAT(24) = 85.455;
CREATE TABLE #result (
    result DECIMAL(7, 2) NOT NULL
);
WITH cte AS (
    SELECT @d * @f AS result
)
INSERT INTO #result
SELECT *
FROM cte;
