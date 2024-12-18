-- tsql sql:
WITH SalesPerson AS (
    SELECT 10000 AS Bonus
    UNION ALL
    SELECT 20000 AS Bonus
    UNION ALL
    SELECT 30000 AS Bonus
)
SELECT STDEVP(Bonus) AS StandardDeviation
FROM SalesPerson;
