--Query type: DQL
WITH temp_result AS (SELECT '123abc' AS str, 'abc' AS chars)
SELECT RTRIM(str, chars)
FROM temp_result
