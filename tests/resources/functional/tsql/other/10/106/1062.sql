-- tsql sql:
WITH SalesPerson AS (
    SELECT SalesQuota, SalesYTD
    FROM (
        VALUES (1, 1000), (2, 2000), (3, 3000)
    ) AS SalesPerson (SalesQuota, SalesYTD)
)
SELECT *
FROM SalesPerson;
