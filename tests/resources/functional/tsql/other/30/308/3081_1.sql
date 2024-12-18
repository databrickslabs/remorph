-- tsql sql:
WITH MyCTE AS (
    SELECT
        BusinessEntityID AS EmpID,
        SalesQuota AS OldSalesQuota,
        SalesQuota * 1.25 AS NewSalesQuota,
        (SalesQuota * 1.25) - SalesQuota AS SalesQuotaDifference,
        GETDATE() AS ModifiedDate
    FROM
    (
        VALUES
            (1, 1000, '2022-01-01'),
            (2, 2000, '2022-01-02'),
            (3, 3000, '2022-01-03'),
            (4, 4000, '2022-01-04'),
            (5, 5000, '2022-01-05'),
            (6, 6000, '2022-01-06'),
            (7, 7000, '2022-01-07'),
            (8, 8000, '2022-01-08'),
            (9, 9000, '2022-01-09'),
            (10, 10000, '2022-01-10')
    ) AS Subquery(BusinessEntityID, SalesQuota, ModifiedDate)
)
SELECT
    EmpID,
    OldSalesQuota,
    NewSalesQuota,
    SalesQuotaDifference,
    ModifiedDate
FROM
    MyCTE;
