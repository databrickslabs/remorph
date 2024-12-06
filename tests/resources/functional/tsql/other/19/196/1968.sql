-- tsql sql:
WITH revenue AS (
    SELECT
        c.c_custkey,
        c.c_name,
        c.c_acctbal,
        c.n_name,
        c.c_address,
        c.c_phone,
        c.c_comment,
        SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue
    FROM (
        VALUES
            (1, 'Customer1', 100.0, 'Nation1', 'Address1', 'Phone1', 'Comment1'),
            (2, 'Customer2', 200.0, 'Nation2', 'Address2', 'Phone2', 'Comment2'),
            (3, 'Customer3', 300.0, 'Nation3', 'Address3', 'Phone3', 'Comment3')
    ) AS c (
        c_custkey,
        c_name,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment
    )
    INNER JOIN (
        VALUES
            (1, 1, 10.0, 0.1),
            (1, 2, 20.0, 0.2),
            (2, 3, 30.0, 0.3)
    ) AS o (
        o_orderkey,
        o_custkey,
        o_totalprice,
        o_discount
    ) ON c.c_custkey = o.o_custkey
    INNER JOIN (
        VALUES
            (1, 1, 100.0, 0.1),
            (1, 2, 200.0, 0.2),
            (2, 3, 300.0, 0.3)
    ) AS l (
        l_orderkey,
        l_linenumber,
        l_extendedprice,
        l_discount
    ) ON o.o_orderkey = l.l_orderkey
    GROUP BY
        c.c_custkey,
        c.c_name,
        c.c_acctbal,
        c.n_name,
        c.c_address,
        c.c_phone,
        c.c_comment
),
revenue_rank AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS row_num
    FROM revenue
)
SELECT *
FROM revenue_rank
WHERE row_num = 1
ORDER BY revenue DESC;
