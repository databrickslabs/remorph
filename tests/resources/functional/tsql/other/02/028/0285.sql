--Query type: DDL
DROP TABLE IF EXISTS customer_aggr;
CREATE TABLE customer_aggr
(
    c_custkey INT,
    c_acctbal DECIMAL(10, 2)
)
WITH (DISTRIBUTION = ROUND_ROBIN);
INSERT INTO customer_aggr (c_custkey, c_acctbal)
SELECT c_custkey, c_acctbal
FROM (
    VALUES (1, 100.00),
           (2, 200.00),
           (3, 300.00)
) AS customer (c_custkey, c_acctbal);
SELECT *
FROM customer_aggr;
-- REMORPH CLEANUP: DROP TABLE customer_aggr;
