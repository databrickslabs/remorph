-- tsql sql:
WITH TempResult AS (SELECT AVG(l_extendedprice) AS [Average extended price], SUM(l_discount) AS [Total discount] FROM lineitem WHERE l_shipinstruct LIKE 'TAKE BACK RETURN%') SELECT * FROM TempResult
