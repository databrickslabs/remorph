-- tsql sql:
WITH SalesData AS (
    SELECT 1 AS OrderID, 100 AS TotalAmount, '2022-01-01' AS OrderDate
    UNION ALL
    SELECT 2, 200, '2022-01-15'
    UNION ALL
    SELECT 3, 50, '2022-02-01'
),
CustomerData AS (
    SELECT 1 AS CustomerID, 'John Doe' AS CustomerName
    UNION ALL
    SELECT 2, 'Jane Doe'
    UNION ALL
    SELECT 3, 'Bob Smith'
)
SELECT
    sd.OrderID,
    cd.CustomerName,
    sd.TotalAmount,
    sd.OrderDate,
    SUM(sd.TotalAmount) OVER (PARTITION BY cd.CustomerID) AS TotalCustomerSales,
    AVG(sd.TotalAmount) OVER () AS AverageSaleAmount
FROM
    SalesData sd
    INNER JOIN CustomerData cd ON sd.OrderID = cd.CustomerID
WHERE
    sd.TotalAmount > 50
ORDER BY
    sd.OrderID
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY;
