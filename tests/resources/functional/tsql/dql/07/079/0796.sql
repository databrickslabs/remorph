--Query type: DQL
SELECT CAST('2022-01-01' AS DATE) AS original_date, REVERSE(CAST('2022-01-01' AS DATE)) AS reversed_date FROM (VALUES (1)) AS temp_result_set(id);
