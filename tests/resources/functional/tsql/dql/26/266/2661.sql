--Query type: DQL
WITH temp_result AS (SELECT 12345 AS num) SELECT num << 5 FROM temp_result
