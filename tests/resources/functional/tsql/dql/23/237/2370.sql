--Query type: DQL
WITH cte AS (
    SELECT name AS collation_name, description
    FROM sys.fn_helpcollations()
)
SELECT *
FROM cte
WHERE collation_name NOT LIKE N'SQL%'
    AND description IS NOT NULL;