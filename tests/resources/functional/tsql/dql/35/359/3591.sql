-- tsql sql:
SELECT s_suppkey, SUBSTRING(s_name, 1, 10) AS supplier_name FROM (VALUES (100000, 'Supplier#000000001'), (100001, 'Supplier#000000002')) AS supplier(s_suppkey, s_name) WHERE s_suppkey = 100000
