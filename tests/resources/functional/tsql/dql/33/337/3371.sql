-- tsql sql:
SELECT p_partkey, p_name FROM (VALUES (1, 'Lock Washer 1'), (2, 'Lock Washer 2'), (3, 'Lock Washer 3')) AS p (p_partkey, p_name) WHERE p_name LIKE 'Lock Washer%' ORDER BY p_partkey DESC;
