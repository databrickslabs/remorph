-- tsql sql:
SELECT * FROM (VALUES (1, 'USA'), (2, 'Canada'), (3, 'Mexico')) AS temp_result (c_custkey, c_nationkey) ORDER BY c_custkey, c_nationkey
