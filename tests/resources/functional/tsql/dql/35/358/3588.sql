-- tsql sql:
WITH customer AS (
    SELECT 1 AS c_custkey, 'Comment1' AS c_comment
    UNION ALL
    SELECT 2, 'Comment2'
)
SELECT c_custkey, CASE WHEN c_comment IS NULL OR c_comment = '' THEN 'Invalid Text Data' ELSE 'Valid Text Data' END AS TextValidation
FROM customer
ORDER BY c_custkey;
