-- tsql sql:
SELECT CAST(CONVERT(VARCHAR(10), T1.c_orderkey) AS BINARY(10)) AS orderkey_binary FROM (VALUES (1), (2), (3)) AS T1 (c_orderkey);
