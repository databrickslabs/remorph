--Query type: DDL
DROP TABLE IF EXISTS customer;
CREATE TABLE customer
(
    c_custkey INT,
    c_name VARCHAR(25),
    c_address VARCHAR(40),
    c_nationkey INT,
    c_phone VARCHAR(15),
    c_acctbal DECIMAL(10, 2),
    c_mktsegment VARCHAR(10),
    c_comment VARCHAR(117)
);
SELECT * FROM customer;
-- REMORPH CLEANUP: DROP TABLE customer;