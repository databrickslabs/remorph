--Query type: DDL
CREATE TABLE customer_temp (c_custkey INT, c_nationkey INT, c_acctbal DECIMAL(10, 2));
WITH temp AS (
    SELECT 1 AS c_custkey, 2 AS c_nationkey, 3.4 AS c_acctbal
)
INSERT INTO customer_temp (c_custkey, c_nationkey, c_acctbal)
SELECT * FROM temp;
SELECT * FROM customer_temp;
-- REMORPH CLEANUP: DROP TABLE customer_temp;