--Query type: DDL
WITH temp_result AS (
    SELECT 1 AS suppkey, 'Supplier#000000001' AS s_name, '25-989-741-2988' AS s_phone, '5% commissions are the norm' AS s_comment, 0.00 AS s_acctbal
    UNION ALL
    SELECT 2 AS suppkey, 'Supplier#000000002' AS s_name, '25-989-741-2989' AS s_phone, '4% commissions are the norm' AS s_comment, 0.00 AS s_acctbal
),
     temp_result2 AS (
    SELECT 1 AS n_nationkey, 'UNITED STATES' AS n_name, 25 AS n_regionkey
    UNION ALL
    SELECT 2 AS n_nationkey, 'CANADA' AS n_name, 1 AS n_regionkey
)
SELECT T1.suppkey, T1.s_name, SUM(T2.l_extendedprice * (1 - T2.l_discount)) AS revenue, T1.s_acctbal, T3.n_name, T1.s_phone, T1.s_comment
FROM temp_result T1
JOIN (
    VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
) T2 (l_suppkey, l_orderkey, l_partkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51)
    ON T1.suppkey = T2.l_suppkey
JOIN temp_result2 T3
    ON T1.suppkey = T3.n_nationkey
WHERE T1.s_acctbal > 0.00
    AND T2.l_orderkey IN (
        SELECT l_orderkey
        FROM (
            VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        ) T4 (l_suppkey, l_orderkey, l_partkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment, col18, col19, col20, col21, col22, col23, col24, col25, col26, col27, col28, col29, col30, col31, col32, col33, col34, col35, col36, col37, col38, col39, col40, col41, col42, col43, col44, col45, col46, col47, col48, col49, col50, col51)
    )
GROUP BY T1.suppkey, T1.s_name, T1.s_acctbal, T3.n_name, T1.s_phone, T1.s_comment
ORDER BY revenue DESC
