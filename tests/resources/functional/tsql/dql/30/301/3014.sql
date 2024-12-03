--Query type: DQL
DECLARE @cos FLOAT;
SET @cos = 0.5;
WITH cte AS (
    SELECT 0.5 AS value
)
SELECT 'The ACOS of the number is: ' + CONVERT(VARCHAR, ACOS((SELECT value FROM cte)))
