--Query type: DCL
DECLARE @revenue DECIMAL(18, 2);
SET @revenue = (
    SELECT SUM(l_extendedprice * (1 - l_discount))
    FROM (
        VALUES (1, 100.00, 0.1),
               (2, 200.00, 0.2)
    ) AS temp_lineitem (l_orderkey, l_extendedprice, l_discount)
    WHERE l_orderkey IN (
        SELECT l_orderkey
        FROM (
            VALUES (1, 100.00, 0.1),
                   (2, 200.00, 0.2)
        ) AS temp_lineitem (l_orderkey, l_extendedprice, l_discount)
        GROUP BY l_orderkey
        HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
    )
);
SELECT @revenue AS revenue;