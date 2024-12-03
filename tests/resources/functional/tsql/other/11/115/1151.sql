--Query type: DDL
DECLARE @SequenceValue DECIMAL(3, 0) = 100;
WITH TempResult AS (
    SELECT @SequenceValue AS SequenceValue
    UNION ALL
    SELECT CAST(SequenceValue + 25 AS DECIMAL(3, 0)) AS SequenceValue
    FROM TempResult
    WHERE SequenceValue < 200
)
SELECT SequenceValue
FROM TempResult
OPTION (MAXRECURSION 0);
