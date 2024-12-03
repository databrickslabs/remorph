--Query type: DQL
WITH temp_result AS (
    SELECT 'é' AS char_value, 233 AS unicode_value
)
SELECT UNICODE(char_value) AS [Extended_ASCII], NCHAR(unicode_value) AS [CHARACTER]
FROM temp_result;
