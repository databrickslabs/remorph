-- tsql sql:
CREATE TABLE SalesOrdersPerYear
WITH (DISTRIBUTION = HASH(SalesPersonID))
AS
WITH SalesPerYear_CTE (SalesPersonID, SalesOrderID, SalesYear)
AS
(
    SELECT SalesPersonID, SalesOrderID, YEAR(OrderDate) AS SalesYear
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (1, 2, '2020-01-15'),
               (2, 3, '2020-02-01'),
               (2, 4, '2020-03-01'),
               (3, 5, '2020-04-01'),
               (3, 6, '2020-05-01')
    ) AS SalesData(SalesPersonID, SalesOrderID, OrderDate)
    WHERE SalesPersonID IS NOT NULL
)
SELECT SalesPersonID, COUNT(SalesOrderID) AS TotalSales, SalesYear
FROM SalesPerYear_CTE
GROUP BY SalesYear, SalesPersonID
ORDER BY SalesPersonID, SalesYear;
