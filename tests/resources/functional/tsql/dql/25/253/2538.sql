--Query type: DQL
WITH SalesData AS (
  SELECT 
    DATEPART(yyyy, OrderDate) AS OrderYear,
    DATEPART(mm, OrderDate) AS OrderMonth,
    DATEPART(dd, OrderDate) AS OrderDay,
    TotalDue
  FROM (
    VALUES 
      ('2007-01-01', 100.00),
      ('2007-01-02', 200.00),
      ('2007-02-01', 300.00),
      ('2007-02-02', 400.00),
      ('2008-01-01', 500.00),
      ('2008-01-02', 600.00),
      ('2008-02-01', 700.00),
      ('2008-02-02', 800.00)
  ) AS Orders (OrderDate, TotalDue)
)
SELECT 
  DATEPART(yyyy, OrderYear) AS N'Year',
  DATEPART(mm, OrderMonth) AS N'Month',
  DATEPART(dd, OrderDay) AS N'Day',
  SUM(TotalDue) AS N'Total Due',
  CAST(GROUPING(OrderDay) AS CHAR(1)) + 
  CAST(GROUPING(OrderMonth) AS CHAR(1)) + 
  CAST(GROUPING(OrderYear) AS CHAR(1)) AS N'Bit Vector(base-2)',
  GROUPING_ID(OrderYear, OrderMonth, OrderDay) AS N'Integer Equivalent',
  CASE 
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 0 THEN N'Year Month Day'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 1 THEN N'Year Month'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 2 THEN N'Year Day'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 3 THEN N'Year'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 4 THEN N'Month Day'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 5 THEN N'Month'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 6 THEN N'Day'
    WHEN GROUPING_ID(OrderYear, OrderMonth, OrderDay) = 7 THEN N'Grand Total'
    ELSE N'Error'
  END AS N'Grouping Level'
FROM SalesData
WHERE OrderYear IN (2007, 2008)
  AND OrderMonth IN (1, 2)
  AND OrderDay IN (1, 2)
GROUP BY CUBE(OrderYear, OrderMonth, OrderDay)
ORDER BY GROUPING_ID(OrderYear, OrderMonth, OrderDay), OrderYear, OrderMonth, OrderDay;