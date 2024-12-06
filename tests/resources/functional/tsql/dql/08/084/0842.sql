-- tsql sql:
WITH temp_result AS (
    SELECT 'John' AS name, 'John likes hockey' AS subject
    UNION ALL
    SELECT 'Jane', 'Jane hates hockey'
    UNION ALL
    SELECT 'Jim', 'Jim loves hockey'
)
SELECT name, subject
FROM temp_result
WHERE subject LIKE '%h%k%' ESCAPE 'h'
ORDER BY 1;
