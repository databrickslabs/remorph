-- tsql sql:
WITH temp_result AS ( SELECT 'John' AS Name, 25 AS Age UNION SELECT 'Alice', 30 ) SELECT * FROM temp_result;
