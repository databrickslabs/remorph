--Query type: DCL
WITH customer AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 1),
            (2, 'Customer2', 2)
    ) AS c (custkey, name, nationkey)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 1000.0),
            (2, 1, 2000.0),
            (3, 2, 500.0)
    ) AS o (orderkey, custkey, totalprice)
)
SELECT
    c.custkey,
    c.name,
    SUM(o.totalprice) AS total_revenue
FROM
    customer c
    INNER JOIN orders o ON c.custkey = o.custkey
WHERE
    c.nationkey = 1
GROUP BY
    c.custkey,
    c.name
ORDER BY
    total_revenue DESC;
