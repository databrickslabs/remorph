-- tsql sql:
WITH Sales AS ( SELECT 10000.0 AS SalesAmountQuota UNION ALL SELECT 20000.0 UNION ALL SELECT 30000.0 UNION ALL SELECT 40000.0 ) SELECT VARP(DISTINCT SalesAmountQuota) AS Unique_Variances, VARP(SalesAmountQuota) AS All_Variances FROM Sales
