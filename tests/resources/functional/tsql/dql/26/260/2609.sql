-- tsql sql:
WITH temp_result AS (SELECT 3000000000 AS bigint_value)
SELECT FORMATMESSAGE('Bigint %I64d', bigint_value)
FROM temp_result;
