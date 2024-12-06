-- tsql sql:
WITH temp_customer AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.0, '123 Main St', '123-456-7890', 'Comment1', 'Nation1'),
            (2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 'Nation2')
    ) AS c (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment, c_nationkey)
),

    temp_nation AS (
    SELECT *
    FROM (
        VALUES
            ('Nation1', 'NationName1'),
            ('Nation2', 'NationName2')
    ) AS n (n_nationkey, n_name)
),

    temp_lineitem AS (
    SELECT *
    FROM (
        VALUES
            (1, 10.0, 0.1),
            (2, 20.0, 0.2)
    ) AS l (l_orderkey, l_extendedprice, l_discount)
)

SELECT
    c.c_custkey,
    c.c_name,
    SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue,
    c.c_acctbal,
    n.n_name,
    c.c_address,
    c.c_phone,
    c.c_comment
FROM
    temp_customer c
    INNER JOIN temp_lineitem l ON c.c_custkey = l.l_orderkey
    INNER JOIN temp_nation n ON c.c_nationkey = n.n_nationkey
GROUP BY
    c.c_custkey,
    c.c_name,
    c.c_acctbal,
    c.c_address,
    c.c_phone,
    n.n_name,
    c.c_comment
HAVING
    c.c_acctbal > (
        SELECT AVG(c_acctbal)
        FROM temp_customer
    )
ORDER BY
    revenue DESC;
