--Query type: DCL
SELECT TOP 10
    c.custkey,
    c.name,
    SUM(o.totalprice) AS total_revenue
FROM
    (
        VALUES
            (1, 'Customer 1', 1),
            (2, 'Customer 2', 2)
    ) c (custkey, name, nationkey)
    INNER JOIN (
        VALUES
            (1, 1, 1000.0),
            (2, 1, 2000.0),
            (3, 2, 500.0)
    ) o (orderid, custkey, totalprice)
    ON c.custkey = o.custkey
WHERE
    c.nationkey = 1
GROUP BY
    c.custkey,
    c.name
HAVING
    SUM(o.totalprice) > 1000000
ORDER BY
    total_revenue DESC;
