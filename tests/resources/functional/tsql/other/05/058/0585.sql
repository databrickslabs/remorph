-- tsql sql:
WITH test_table AS (
    SELECT 'comment1' AS o_comment
    UNION ALL
    SELECT 'comment2' AS o_comment
)
SELECT *
FROM test_table;
