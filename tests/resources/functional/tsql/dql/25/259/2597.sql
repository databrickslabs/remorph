-- tsql sql:
WITH ProductCTE AS ( SELECT 'Road-250' AS ProductName, 300.00 AS ListPrice UNION ALL SELECT 'Road-150' AS ProductName, 400.00 AS ListPrice ) SELECT ProductName, ListPrice FROM ProductCTE WHERE CONVERT(VARCHAR(10), ListPrice) LIKE '3%';
