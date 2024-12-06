-- tsql sql:
SELECT c_custkey FROM (VALUES (1, 10), (2, 20), (3, 30)) AS C (c_custkey, c_nationkey) WHERE c_nationkey < 25
