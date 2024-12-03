--Query type: DQL
SELECT CASE WHEN TRY_CONVERT(float, T1.c_acctbal) IS NULL THEN 'Cast failed' ELSE 'Cast succeeded' END AS Result FROM (VALUES (1, 100.0), (2, 200.0), (3, 'test')) AS T1 (c_custkey, c_acctbal);
