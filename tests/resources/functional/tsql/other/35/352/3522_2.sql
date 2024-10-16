--Query type: DDL
WITH temp_result AS (
    SELECT 
        1 AS c_custkey,
        'Customer 1' AS c_name,
        1000.00 AS c_acctbal,
        'Nation 1' AS n_name,
        'Address 1' AS c_address,
        'Phone 1' AS c_phone,
        'Comment 1' AS c_comment,
        100.00 AS l_extendedprice,
        0.10 AS l_discount,
        1 AS l_orderkey
    UNION ALL
    SELECT 
        2 AS c_custkey,
        'Customer 2' AS c_name,
        2000.00 AS c_acctbal,
        'Nation 2' AS n_name,
        'Address 2' AS c_address,
        'Phone 2' AS c_phone,
        'Comment 2' AS c_comment,
        200.00 AS l_extendedprice,
        0.20 AS l_discount,
        2 AS l_orderkey
),

-- Create a temporary result set to filter l_orderkey

temp_result2 AS (
    SELECT 
        l_orderkey,
        SUM(l_extendedprice * (1 - l_discount)) AS revenue
    FROM 
        (VALUES 
            (1, 100.00, 0.10, 1),
            (2, 200.00, 0.20, 2)
        ) AS temp_result3 (l_orderkey, l_extendedprice, l_discount, o_custkey)
    GROUP BY 
        l_orderkey
    HAVING 
        SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)

SELECT 
    c_custkey,
    c_name,
    SUM(tr.l_extendedprice * (1 - tr.l_discount)) AS revenue,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
FROM 
    temp_result tr
JOIN 
    (VALUES 
        (1, 100.00, 0.10, 1),
        (2, 200.00, 0.20, 2)
    ) AS temp_result4 (l_orderkey, l_extendedprice, l_discount, o_custkey)
    ON tr.c_custkey = temp_result4.o_custkey
WHERE 
    tr.c_acctbal > 0.00
    AND temp_result4.l_orderkey IN (
        SELECT 
            l_orderkey
        FROM 
            temp_result2
    )
GROUP BY 
    tr.c_custkey, 
    tr.c_name, 
    tr.c_acctbal, 
    tr.n_name, 
    tr.c_address, 
    tr.c_phone, 
    tr.c_comment
ORDER BY 
    revenue DESC;