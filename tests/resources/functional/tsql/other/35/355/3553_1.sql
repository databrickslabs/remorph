--Query type: DCL
WITH temp_result AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, 'USA', '123 Main St', '123-456-7890', 'This is a comment'),
            (2, 'Customer2', 200.00, 'Canada', '456 Elm St', '987-654-3210', 'This is another comment')
    ) AS t (custkey, name, acctbal, nation, address, phone, comment)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, 100.00),
            (2, 2, 200.00)
    ) AS t (orderkey, custkey, totalprice)
),
lineitem AS (
    SELECT *
    FROM (
        VALUES
            (1, 10.00, 0.10),
            (2, 20.00, 0.20)
    ) AS t (orderkey, extendedprice, discount)
)
SELECT
    t.custkey,
    t.name,
    SUM(l.extendedprice * (1 - l.discount)) AS revenue,
    t.acctbal,
    t.nation,
    t.address,
    t.phone,
    t.comment
FROM
    temp_result t
    INNER JOIN orders o ON t.custkey = o.custkey
    INNER JOIN lineitem l ON o.orderkey = l.orderkey
WHERE
    t.acctbal > 0.00
GROUP BY
    t.custkey,
    t.name,
    t.acctbal,
    t.nation,
    t.address,
    t.phone,
    t.comment
ORDER BY
    revenue DESC
