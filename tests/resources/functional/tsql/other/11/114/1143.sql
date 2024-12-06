-- tsql sql:
WITH OrdersCTE AS (
    SELECT 1 AS O_ORDERKEY, 10 AS O_CUSTKEY
    UNION ALL
    SELECT 2, 20
    UNION ALL
    SELECT 3, 30
)
SELECT *
FROM OrdersCTE
WHERE O_CUSTKEY = 10;
