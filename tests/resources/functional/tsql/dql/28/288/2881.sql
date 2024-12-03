--Query type: DQL
WITH customer_info AS (
    SELECT c_name, c_custkey, c_nationkey
    FROM (
        VALUES ('Customer#000000001', 1, 1),
               ('Customer#000000002', 2, 2)
    ) AS c (c_name, c_custkey, c_nationkey)
),

nation_info AS (
    SELECT n_name, n_nationkey
    FROM (
        VALUES ('ALGERIA', 1),
               ('ARGENTINA', 2)
    ) AS n (n_name, n_nationkey)
)

SELECT ci.c_name, ni.n_name
FROM customer_info AS ci
JOIN nation_info AS ni ON ci.c_nationkey = ni.n_nationkey
