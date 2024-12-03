--Query type: DQL
WITH ErrorData AS (
    SELECT 1 AS ErrorID, 'Error 1' AS ErrorMessage
    UNION ALL
    SELECT 2 AS ErrorID, 'Error 2' AS ErrorMessage
)
SELECT COUNT(ed.ErrorID) AS TotalErrors, GETDATE() AS AsOfDate
FROM ErrorData ed;
