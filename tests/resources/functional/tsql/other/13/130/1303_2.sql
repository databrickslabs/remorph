-- tsql sql:
WITH lineitem AS (
    SELECT orderkey, shipdate, CAST(GETDATE() AS smalldatetime) AS ShippedDate
    FROM (
        VALUES (1, '2022-01-01')
    ) AS data (orderkey, shipdate)
)
SELECT *
FROM lineitem;
