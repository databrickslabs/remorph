--Query type: DDL
WITH temp_result AS ( SELECT id FROM (VALUES (1)) AS t(id) ) SELECT * INTO #temp_result FROM temp_result;
