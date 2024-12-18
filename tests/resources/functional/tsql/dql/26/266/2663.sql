-- tsql sql:
WITH temp_result AS (SELECT EXP(10) AS exp_value)
SELECT LOG(exp_value)
FROM temp_result
