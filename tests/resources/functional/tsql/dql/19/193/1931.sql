-- tsql sql:
WITH temp_result AS (SELECT CAST(GETDATE() AS datetime) AS current_date_value)
SELECT GETDATE() AS default_value, current_date_value
FROM temp_result
