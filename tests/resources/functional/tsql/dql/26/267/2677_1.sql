--Query type: DQL
WITH temp_result AS (SELECT NCHAR(504) COLLATE Latin1_General_CI_AS AS char_value, NCHAR(504) COLLATE Latin1_General_100_CI_AS AS char_value2)
SELECT LOWER(char_value) AS [Version80Collation], LOWER(char_value2) AS [Version100Collation]
FROM temp_result
