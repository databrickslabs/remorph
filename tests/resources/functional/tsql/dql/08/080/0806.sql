-- tsql sql:
WITH temp_result AS (
    SELECT 'a' AS char_lower, 'z' AS char_upper
    UNION ALL
    SELECT 'A', 'Z'
),
bounds AS (
    SELECT MIN(LOWER(char_lower) COLLATE Latin1_General_CI_AS) AS lower_bound,
           MAX(LOWER(char_upper) COLLATE Latin1_General_CI_AS) AS upper_bound
    FROM temp_result
)
SELECT CASE
        WHEN 'm' BETWEEN lower_bound AND upper_bound THEN 1
        ELSE 0
    END AS result
FROM bounds
