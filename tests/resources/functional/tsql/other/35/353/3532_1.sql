--Query type: DCL
CREATE PROCEDURE GetSupplierRevenue
AS
BEGIN
    WITH temp_result AS (
        SELECT 1001 AS suppkey, 'Supplier#000000001' AS s_name, 1000.00 AS s_acctbal, '25-989-741-2988' AS s_phone, 'Comment for Supplier#000000001' AS s_comment, 5 AS n_nationkey, 'UNITED STATES' AS n_name, 'United States' AS r_name
        UNION ALL
        SELECT 1002 AS suppkey, 'Supplier#000000002' AS s_name, 2000.00 AS s_acctbal, '25-989-741-2999' AS s_phone, 'Comment for Supplier#000000002' AS s_comment, 5 AS n_nationkey, 'UNITED STATES' AS n_name, 'United States' AS r_name
    ),
    temp_result2 AS (
        SELECT 1001 AS suppkey, 1001 AS o_orderkey, 1000.00 AS l_extendedprice, 0.10 AS l_discount
        UNION ALL
        SELECT 1002 AS suppkey, 1002 AS o_orderkey, 2000.00 AS l_extendedprice, 0.20 AS l_discount
    )
    SELECT T1.suppkey, T1.s_name, SUM(T2.l_extendedprice * (1 - T2.l_discount)) AS revenue, T1.s_acctbal, T1.n_name, T1.s_phone, T1.s_comment
    FROM temp_result T1
    JOIN temp_result2 T2 ON T1.suppkey = T2.suppkey
    WHERE T1.s_acctbal > 0.00 AND T2.o_orderkey IN (
        SELECT o_orderkey FROM temp_result2
        GROUP BY o_orderkey
        HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
    )
    GROUP BY T1.suppkey, T1.s_name, T1.s_acctbal, T1.n_name, T1.s_phone, T1.s_comment
    ORDER BY revenue DESC;
END;
