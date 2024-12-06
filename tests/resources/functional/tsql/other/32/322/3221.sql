-- tsql sql:
WITH t AS (
    SELECT l_extendedprice
    FROM (
        VALUES
            (1),
            (2),
            (3),
            (4),
            (5),
            (6),
            (7),
            (8),
            (9),
            (10),
            (11)
    ) AS t (l_extendedprice)
),
aggregates AS (
    SELECT
        SUM(CASE WHEN l_extendedprice > 10 THEN 1 ELSE 0 END) AS high_count,
        SUM(CASE WHEN l_extendedprice < 0 THEN 1 ELSE 0 END) AS low_count,
        SUM(l_extendedprice) AS total_sum,
        AVG(l_extendedprice) AS average,
        MAX(l_extendedprice) AS max_value,
        MIN(l_extendedprice) AS min_value,
        COUNT(l_extendedprice) AS count_value
    FROM
        t
)
SELECT
    high_count,
    low_count,
    total_sum,
    average,
    max_value,
    min_value,
    count_value,
    NULL AS rank_value,
    NULL AS dense_rank_value,
    NULL AS row_number_value,
    NULL AS ntile_value,
    NULL AS lag_value,
    NULL AS lead_value,
    NULL AS first_value,
    NULL AS last_value
FROM
    aggregates;
