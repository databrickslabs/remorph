--Query type: DDL
CREATE TABLE #customer_mv
(
    c_custkey INT,
    c_name VARCHAR(50),
    c_address VARCHAR(100)
);

INSERT INTO #customer_mv (c_custkey, c_name, c_address)
VALUES
    (1, 'Customer1', 'Address1'),
    (2, 'Customer2', 'Address2');

CREATE CLUSTERED INDEX idx_c_custkey
ON #customer_mv (c_custkey);

SELECT *
FROM #customer_mv;

-- REMORPH CLEANUP: DROP TABLE #customer_mv;
