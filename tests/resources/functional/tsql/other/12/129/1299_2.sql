--Query type: DDL
DROP TABLE #SalesReport;

WITH SalesData AS (
    SELECT 'ProductA' AS Product, 100 AS Price, 5 AS Quantity
    UNION ALL
    SELECT 'ProductB', 200, 3
    UNION ALL
    SELECT 'ProductC', 50, 10
),

RankedSales AS (
    SELECT Product, Price, Quantity,
           ROW_NUMBER() OVER (ORDER BY Price DESC) AS RowNum,
           RANK() OVER (ORDER BY Price DESC) AS RankNum
    FROM SalesData
),

TotalSales AS (
    SELECT SUM(Price * Quantity) AS TotalRevenue, AVG(Price) AS AveragePrice
    FROM SalesData
)

SELECT 'Total Revenue: ' + CONVERT(VARCHAR, (SELECT TotalRevenue FROM TotalSales)) + ', Average Price: ' + CONVERT(VARCHAR, (SELECT AveragePrice FROM TotalSales)) AS SalesSummary,
       (SELECT Product + ' - ' + CONVERT(VARCHAR, Price) + ' - ' + CONVERT(VARCHAR, Quantity) FROM RankedSales WHERE RowNum = 1) AS TopProduct,
       (SELECT 'Rank ' + CONVERT(VARCHAR, RankNum) + ': ' + Product FROM RankedSales WHERE RankNum = 1) AS TopRankedProduct
FOR JSON PATH, ROOT('SalesReport');