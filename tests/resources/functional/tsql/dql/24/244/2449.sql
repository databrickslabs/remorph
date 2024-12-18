-- tsql sql:
WITH temp_result AS (
    SELECT CAST(0.0000009000 AS DECIMAL(30, 10)) AS decimal_value1,
           CAST(1.0000000000 AS DECIMAL(30, 10)) AS decimal_value2
)
SELECT CAST(decimal_value1 * decimal_value2 AS DECIMAL(38, 6)) AS result
FROM temp_result;
