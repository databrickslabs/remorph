--Query type: DDL
WITH temp_result AS (
    SELECT
        c_custkey,
        c_name,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment,
        l_extendedprice,
        l_discount,
        l_orderkey
    FROM (
        VALUES
            (1, 'Customer1', 1000.00, 'USA', '123 Main St', '123-456-7890', 'This is a comment', 100.00, 0.10, 1),
            (2, 'Customer2', 2000.00, 'Canada', '456 Elm St', '987-654-3210', 'This is another comment', 200.00, 0.20, 2)
    ) AS temp_result (
        c_custkey,
        c_name,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment,
        l_extendedprice,
        l_discount,
        l_orderkey
    )
)
SELECT
    c_custkey,
    c_name,
    SUM(l_extendedprice * (1 - l_discount)) AS revenue,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
FROM temp_result
WHERE c_acctbal > 0.00
    AND l_orderkey IN (
        SELECT l_orderkey
        FROM temp_result
        GROUP BY l_orderkey
        HAVING SUM(l_extendedprice * (1 - l_discount)) > 100.00
    )
GROUP BY
    c_custkey,
    c_name,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
ORDER BY revenue DESC;