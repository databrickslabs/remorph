--Query type: DDL
SELECT * FROM (VALUES ('a-1'), ('b-2'), ('c-3')) AS temp_result(value) WHERE value LIKE '[a-z]-%[0-9]';