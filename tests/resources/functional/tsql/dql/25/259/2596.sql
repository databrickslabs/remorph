--Query type: DQL
WITH products AS ( SELECT 'Product A' AS ProductName, 30.00 AS ListPrice UNION ALL SELECT 'Product B', 25.00 UNION ALL SELECT 'Product C', 35.00 ) SELECT ProductName, ListPrice FROM products WHERE CAST(ListPrice AS int) LIKE '3%';
