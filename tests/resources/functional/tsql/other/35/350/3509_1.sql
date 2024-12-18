-- tsql sql:
SELECT TOP 10
    c.custkey,
    c.name,
    SUM(o.totalprice) AS total_revenue
FROM
    (
        VALUES
            (1, 'Customer 1'),
            (2, 'Customer 2'),
            (3, 'Customer 3')
    ) c (custkey, name)
    INNER JOIN (
        VALUES
            (1, 1, 1000.0),
            (2, 1, 2000.0),
            (3, 2, 3000.0)
    ) o (orderkey, custkey, totalprice)
    ON c.custkey = o.custkey
WHERE
    o.orderkey IN (
        SELECT orderkey
        FROM (
            VALUES
                (1, 1, 1000.0),
                (2, 1, 2000.0),
                (3, 2, 3000.0)
        ) o (orderkey, custkey, totalprice)
        WHERE totalprice > 500.0
    )
GROUP BY
    c.custkey,
    c.name
HAVING
    SUM(o.totalprice) > 1000000
ORDER BY
    total_revenue DESC;
