-- tsql sql:
WITH SalesData AS (
    SELECT CAST(ROW_NUMBER() OVER (ORDER BY o_orderkey) AS INT) AS OrderDateKey,
           CAST(o_totalprice * (1 - o_discount) AS DECIMAL(10, 2)) AS SalesAmount
    FROM (
        VALUES (1, 100.00, 0.05),
               (2, 200.00, 0.10),
               (3, 300.00, 0.15),
               (4, 400.00, 0.20),
               (5, 500.00, 0.25)
    ) AS Orders (o_orderkey, o_totalprice, o_discount)
)
SELECT OrderDateKey,
       SUM(SalesAmount) AS TotalSales
FROM SalesData
GROUP BY OrderDateKey
ORDER BY OrderDateKey;
