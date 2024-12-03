--Query type: DML
DECLARE @StartingRowNumber INT = 1, @RowCountPerPage INT = 3;

WITH SalesOrder AS (
    SELECT SalesOrderID, CustomerID, OrderDate, ROW_NUMBER() OVER (ORDER BY SalesOrderID) AS RowNum
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 1, '2020-01-15'),
               (3, 2, '2020-02-01'),
               (4, 3, '2020-03-01'),
               (5, 1, '2020-04-01'),
               (6, 2, '2020-05-01'),
               (7, 3, '2020-06-01'),
               (8, 1, '2020-07-01'),
               (9, 2, '2020-08-01'),
               (10, 3, '2020-09-01')
    ) AS SalesOrder(SalesOrderID, CustomerID, OrderDate)
),
RecursiveCTE AS (
    SELECT SalesOrderID, CustomerID, OrderDate, RowNum, 1 AS PageNum
    FROM SalesOrder
    WHERE RowNum BETWEEN @StartingRowNumber AND @StartingRowNumber + @RowCountPerPage - 1
    UNION ALL
    SELECT s.SalesOrderID, s.CustomerID, s.OrderDate, s.RowNum, r.PageNum + 1
    FROM SalesOrder s
    INNER JOIN RecursiveCTE r ON s.RowNum = r.RowNum + @RowCountPerPage
)

SELECT SalesOrderID, CustomerID, OrderDate
FROM RecursiveCTE
ORDER BY PageNum, RowNum
OPTION (MAXRECURSION 0);
