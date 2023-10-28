-- Uses AdventureWorks  
  
SELECT OrderDateKey, DueDateKey, SUM(SalesAmount) AS TotalSales   
FROM FactInternetSales
GROUP BY OrderDateKey, DueDateKey   
ORDER BY OrderDateKey;