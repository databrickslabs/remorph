--Query type: DQL
WITH temp_result_set AS (
    SELECT *
    FROM (
        VALUES
            (1, 'a', 'x'),
            (2, 'b', 'y'),
            (3, 'c', 'z'),
            (4, 'd', 'w')
    ) AS temp (col1, col2, col3)
)
SELECT *
FROM temp_result_set
ORDER BY col1, col2, col3;