-- tsql sql:
WITH Dates AS (
    SELECT CAST('2022-01-01' AS DATE) AS DateValue
)
SELECT
    FORMAT(DateValue, 'D', 'en-US') AS [US English],
    FORMAT(DateValue, 'D', 'en-gb') AS [British English],
    FORMAT(DateValue, 'D', 'de-de') AS [German],
    FORMAT(DateValue, 'D', 'zh-cn') AS [Chinese Simplified (PRC)]
FROM Dates;
