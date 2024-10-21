--Query type: DQL
WITH OrdersCTE AS (
    SELECT CAST(ORDERDATE AS DATE) AS OrderDate,
           TOTALPRICE AS TotalDue
    FROM ORDERS
)
SELECT DATEPART(yyyy, OrderDate) AS N'Order Year',
       SUM(TotalDue) AS N'Total Order Value'
FROM OrdersCTE
GROUP BY DATEPART(yyyy, OrderDate)
ORDER BY DATEPART(yyyy, OrderDate);