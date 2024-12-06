-- tsql sql:
WITH dates AS (
    SELECT '1992-01-01' AS order_date
    UNION ALL
    SELECT '1993-01-01' AS order_date
    UNION ALL
    SELECT '1994-01-01' AS order_date
)
SELECT DATEADD(year, 1, order_date) AS new_order_date
FROM dates
