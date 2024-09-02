--Query type: DML
WITH TempResult AS (
    SELECT 'abc' AS StringValue, NULL AS NullValue
)
SELECT StringValue + ISNULL(NullValue, '') AS ResultWhen_OFF
FROM TempResult;