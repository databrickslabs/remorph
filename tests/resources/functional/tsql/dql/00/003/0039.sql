--Query type: DQL
WITH temp_result AS (
    SELECT 'USA' AS n_name, 'North America' AS r_name
    UNION ALL
    SELECT 'Canada', 'North America'
)
SELECT n_name, r_name
FROM temp_result;
