-- tsql sql:
SELECT c_custkey, c_name, c_address FROM (VALUES (1, 'John', '123 Street'), (2, 'Jane', NULL)) AS temp_result(c_custkey, c_name, c_address) WHERE c_custkey IS NOT NULL OR c_name IS NULL ORDER BY c_custkey;
