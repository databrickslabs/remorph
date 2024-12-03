--Query type: DQL
WITH orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 100.0),
            (2, 200.0),
            (3, 300.0)
    ) AS orders (o_custkey, o_totalprice)
),
 customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1'),
            (2, 'Customer2'),
            (3, 'Customer3')
    ) AS customers (c_custkey, c_name)
)
SELECT
    c_custkey,
    SUM(o_totalprice) AS total_sales
FROM
    orders
INNER JOIN customers
    ON c_custkey = o_custkey
GROUP BY
    c_custkey
