-- tsql sql:
WITH sales_data AS (
    SELECT
        c_custkey,
        o_orderkey,
        o_orderdate,
        l_extendedprice * (1 - l_discount) AS sales_amount
    FROM
        (
            VALUES
                (1, 1, '2020-01-01', 100.00, 0.1),
                (1, 2, '2020-01-15', 200.00, 0.2),
                (2, 3, '2020-02-01', 50.00, 0.05)
        ) AS lineitem (
            c_custkey,
            o_orderkey,
            o_orderdate,
            l_extendedprice,
            l_discount
        )
)
SELECT
    c_custkey,
    DATEPART(yy, o_orderdate) AS sales_year,
    CONVERT(VARCHAR(20), sales_amount, 1) AS sales_amount,
    CONVERT(VARCHAR(20), AVG(sales_amount) OVER (PARTITION BY c_custkey ORDER BY DATEPART(yy, o_orderdate)), 1) AS moving_avg,
    CONVERT(VARCHAR(20), SUM(sales_amount) OVER (PARTITION BY c_custkey ORDER BY DATEPART(yy, o_orderdate)), 1) AS cumulative_total
FROM
    sales_data
WHERE
    c_custkey IS NULL OR c_custkey < 5
ORDER BY
    c_custkey,
    sales_year;
