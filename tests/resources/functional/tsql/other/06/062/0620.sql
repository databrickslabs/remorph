--Query type: DDL
CREATE TABLE #mv_customer
(
    c_custkey INT,
    c_name VARCHAR(50),
    c_address VARCHAR(100)
);

INSERT INTO #mv_customer (c_custkey, c_name, c_address)
VALUES
    (1, 'Customer1', 'Address1'),
    (2, 'Customer2', 'Address2');

SELECT *
FROM #mv_customer;

DROP TABLE #mv_customer;
-- REMORPH CLEANUP: DROP TABLE #mv_customer;
