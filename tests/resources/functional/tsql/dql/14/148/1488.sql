-- tsql sql:
WITH TempResult AS (
    SELECT 1 AS NewScrapReasonID, 'Reason1' AS Name, '2022-01-01' AS ModifiedDate
    UNION ALL
    SELECT 2, 'Reason2', '2022-01-02'
),
TempResult2 AS (
    SELECT 3 AS ScrapReasonID, 'Reason3' AS Name, '2022-01-03' AS ModifiedDate
    UNION ALL
    SELECT 4, 'Reason4', '2022-01-04'
)
SELECT NewScrapReasonID, Name, ModifiedDate
FROM TempResult;

SELECT ScrapReasonID, Name, ModifiedDate
FROM TempResult2
