--Query type: DCL
WITH temp_result AS (
    SELECT 1 AS suppkey, 'Supplier#000000001' AS s_name, 1000.00 AS s_acctbal, 1 AS s_nationkey, 'Address1' AS s_address, 'Phone1' AS s_phone, 'Comment1' AS s_comment
    UNION ALL
    SELECT 2 AS suppkey, 'Supplier#000000002' AS s_name, 2000.00 AS s_acctbal, 1 AS s_nationkey, 'Address2' AS s_address, 'Phone2' AS s_phone, 'Comment2' AS s_comment
),

    temp_result2 AS (
    SELECT 1 AS l_suppkey, 100.00 AS l_extendedprice, 0.1 AS l_discount
    UNION ALL
    SELECT 2 AS l_suppkey, 200.00 AS l_extendedprice, 0.2 AS l_discount
),

    temp_result3 AS (
    SELECT l_suppkey
    FROM temp_result2
    GROUP BY l_suppkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)

SELECT 
    T1.suppkey, 
    T1.s_name, 
    SUM(T2.l_extendedprice * (1 - T2.l_discount)) AS revenue, 
    T1.s_acctbal, 
    T3.n_name, 
    T1.s_address, 
    T1.s_phone, 
    T1.s_comment
FROM 
    temp_result AS T1
JOIN 
    temp_result2 AS T2 ON T1.suppkey = T2.l_suppkey
JOIN 
    (VALUES (1, 'Nation#1')) AS T3 (n_nationkey, n_name) ON T1.s_nationkey = T3.n_nationkey
WHERE 
    T1.s_acctbal > 0.00 
    AND T2.l_suppkey IN (SELECT l_suppkey FROM temp_result3)
GROUP BY 
    T1.suppkey, 
    T1.s_name, 
    T1.s_acctbal, 
    T3.n_name, 
    T1.s_address, 
    T1.s_phone, 
    T1.s_comment
ORDER BY 
    revenue DESC;