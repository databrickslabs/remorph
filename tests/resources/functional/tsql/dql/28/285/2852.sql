-- tsql sql:
WITH temp_result AS ( SELECT 45 AS num1, 30 AS num2 ) SELECT IIF(num1 > num2, CAST(NULL AS INT), CAST(NULL AS INT)) AS [Result] FROM temp_result
