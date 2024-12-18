-- tsql sql:
DECLARE @revenue DECIMAL(18, 2);

WITH lineitem_data AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES (
            (1, 1, 100.00, 0.1),
            (2, 1, 20.00, 0.2)
        )
    ) AS lineitem_data(l_orderkey, l_extendedprice, l_discount, l_unused_column)
),
order_data AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (
            (1, 1, 1000.00),
            (2, 1, 2000.00)
        )
    ) AS order_data(o_orderkey, o_custkey, o_totalprice)
),
customer_data AS (
    SELECT c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment
    FROM (
        VALUES (
            (1, 'Customer1', 100.00, 'Address1', 'Phone1', 'Comment1'),
            (2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2')
        )
    ) AS customer_data(c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment)
),
nation_data AS (
    SELECT n_nationkey, n_name
    FROM (
        VALUES (
            (1, 'Nation1')
        )
    ) AS nation_data(n_nationkey, n_name)
)
SELECT @revenue = SUM(l_extendedprice * (1 - l_discount))
FROM lineitem_data
JOIN order_data ON lineitem_data.l_orderkey = order_data.o_orderkey
JOIN customer_data ON order_data.o_custkey = customer_data.c_custkey
JOIN nation_data ON customer_data.c_custkey = nation_data.n_nationkey
WHERE customer_data.c_acctbal > 0.00
AND lineitem_data.l_orderkey IN (
    SELECT l_orderkey
    FROM lineitem_data
    GROUP BY l_orderkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
GROUP BY customer_data.c_custkey, customer_data.c_name, customer_data.c_acctbal, nation_data.n_name, customer_data.c_address, customer_data.c_phone, customer_data.c_comment
ORDER BY SUM(l_extendedprice * (1 - l_discount)) DESC;

SELECT @revenue AS revenue;
