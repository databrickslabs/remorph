-- tsql sql:
DECLARE @NewPercentage DECIMAL(5, 2);
SET @NewPercentage = 0.2;
SELECT 'NewResult' AS NewColumnName, @NewPercentage AS NewColumnValue, 'This is another test' AS NewDescription
FROM (
    VALUES (1)
) AS NewTemporaryResult(NewTemporaryColumn);
-- REMORPH CLEANUP: DROP TABLE NewTemporaryResult;
