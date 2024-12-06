-- tsql sql:
WITH Sales AS ( SELECT 'SO53115' AS SalesOrderNumber, 1 AS ProductKey UNION ALL SELECT 'SO55981', 2 ) SELECT DISTINCT COUNT(ProductKey) OVER ( PARTITION BY SalesOrderNumber ) AS ProductCount, SalesOrderNumber FROM Sales WHERE SalesOrderNumber IN ( 'SO53115', 'SO55981' );
