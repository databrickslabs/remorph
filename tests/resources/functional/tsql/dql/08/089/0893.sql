-- tsql sql:
WITH temp_result AS ( SELECT 'John' AS name, 25 AS age UNION ALL SELECT 'Jane', 30 ) SELECT * FROM temp_result;
