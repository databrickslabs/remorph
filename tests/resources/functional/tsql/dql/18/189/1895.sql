--Query type: DQL
WITH temp_result AS (SELECT CAST('12:10:16.1234567' AS time(7)) AS time_value, CAST(CAST('12:10:16.1234567' AS time(7)) AS datetime2) AS datetime2_value)
SELECT datetime2_value AS '@datetime2', time_value AS '@time'
FROM temp_result;
