-- tsql sql:
WITH CustomerCTE AS (SELECT 'Customer#000000001' AS c_name, 'United States' AS c_nationkey), NationCTE AS (SELECT 'United States' AS n_name, 1 AS n_nationkey) SELECT T1.c_name FROM CustomerCTE AS T1 INNER JOIN NationCTE AS T2 ON T1.c_nationkey = T2.n_nationkey WHERE T1.c_name = 'Customer#000000001';