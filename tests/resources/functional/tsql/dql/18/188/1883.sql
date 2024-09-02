--Query type: DQL
WITH temp_result AS (SELECT '     Five spaces are at the beginning of this string.' AS original_string)
SELECT original_string AS [Original string], LTRIM(original_string) AS [Without spaces]
FROM temp_result;