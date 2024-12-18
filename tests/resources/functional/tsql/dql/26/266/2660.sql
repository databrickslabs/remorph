-- tsql sql:
SELECT LEFT(c_name, 5) AS short_name FROM (VALUES ('Customer#000000001', 1), ('Customer#000000002', 2), ('Customer#000000003', 3)) AS customers (c_name, c_id) ORDER BY c_id;
