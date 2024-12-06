-- tsql sql:
DECLARE @PredictionA DECIMAL(2, 1) = 0.7;
DECLARE @PredictionB DECIMAL(3, 1) = 0.65;

WITH TempResult AS (
    SELECT 0.5 AS VarX, 0.6 AS Correlation
    UNION ALL
    SELECT 0.7 AS VarX, 0.8 AS Correlation
)

SELECT VarX, Correlation
FROM TempResult
WHERE Correlation < ( SELECT LEAST(@PredictionA, @PredictionB) );
