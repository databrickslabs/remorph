--Query type: DDL
CREATE TABLE #temp_result
(
    s_suppkey INT,
    s_name VARCHAR(255),
    s_address VARCHAR(255),
    s_phone VARCHAR(255),
    s_comment VARCHAR(255),
    l_extendedprice DECIMAL(10, 2),
    l_discount DECIMAL(10, 2),
    o_orderkey INT,
    l_orderkey INT
);

INSERT INTO #temp_result
(
    s_suppkey,
    s_name,
    s_address,
    s_phone,
    s_comment,
    l_extendedprice,
    l_discount,
    o_orderkey,
    l_orderkey
)
VALUES
(
    1,
    'Supplier 1',
    'Address 1',
    'Phone 1',
    'Comment 1',
    100.00,
    0.10,
    1,
    1
),
(
    2,
    'Supplier 2',
    'Address 2',
    'Phone 2',
    'Comment 2',
    200.00,
    0.20,
    2,
    2
);

WITH filtered_result AS
(
    SELECT l_orderkey
    FROM #temp_result
    GROUP BY l_orderkey
    HAVING SUM(l_extendedprice * (1 - l_discount)) > 100000.00
)
SELECT s_suppkey, s_name, SUM(l_extendedprice * (1 - l_discount)) AS revenue, s_address, s_phone, s_comment
FROM #temp_result
WHERE l_discount > 0.00 AND l_orderkey IN (SELECT l_orderkey FROM filtered_result)
GROUP BY s_suppkey, s_name, s_address, s_phone, s_comment
ORDER BY revenue DESC;

SELECT * FROM #temp_result;

DROP TABLE #temp_result;