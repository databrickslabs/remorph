--Query type: DQL
WITH temp_result AS (SELECT 256 AS key_id)
SELECT SYMKEYPROPERTY(key_id, 'algorithm_desc') AS Algorithm
FROM temp_result;