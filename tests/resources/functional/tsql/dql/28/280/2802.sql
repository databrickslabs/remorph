--Query type: DQL
WITH temp_result AS (SELECT CAST(1 AS FLOAT) AS num)
SELECT TAN(PI() * num / 2)
FROM temp_result;