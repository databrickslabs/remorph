-- tsql sql:
WITH T1 AS (SELECT 1 AS o_orderkey, 2 AS l_orderkey, 3.0 AS o_totalprice, 4.0 AS l_extendedprice, 5.0 AS l_quantity, 'a' AS c_name, 'b' AS c_address, 'c' AS c_phone)
SELECT CONVERT(VARCHAR, o_orderkey) AS [ARRAY1], CONVERT(VARCHAR, l_orderkey) AS [ARRAY2], CASE WHEN o_totalprice > 100 THEN 1 ELSE 0 END AS [BOOLEAN], SUBSTRING(c_name, 1, 1) AS [CHAR], CONVERT(DECIMAL(10, 2), o_totalprice) AS [DECIMAL], l_extendedprice AS [DOUBLE], l_quantity AS [INTEGER], (SELECT TOP 1 c_name FROM T1 WHERE c_name = 'a') AS [OBJECT], (SELECT TOP 1 c_name FROM T1 WHERE c_name = 'a') AS [OBJECT AS ARRAY]
FROM T1;
