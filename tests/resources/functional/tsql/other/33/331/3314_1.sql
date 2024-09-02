--Query type: DDL
IF OBJECT_ID(N'customer_temp', N'U') IS NOT NULL
    DROP TABLE customer_temp;

CREATE TABLE customer_temp
(
    c_custkey INT,
    c_name VARCHAR(25),
    c_address VARCHAR(40),
    c_nationkey INT,
    c_phone VARCHAR(15),
    c_acctbal DECIMAL(15, 2),
    c_mktsegment VARCHAR(10),
    c_comment VARCHAR(117)
);

IF OBJECT_ID(N'orders_temp', N'U') IS NOT NULL
    DROP TABLE orders_temp;

CREATE TABLE orders_temp
(
    o_orderkey INT,
    o_custkey INT,
    o_orderstatus VARCHAR(1),
    o_totalprice DECIMAL(15, 2),
    o_orderdate DATE,
    o_orderpriority VARCHAR(15),
    o_clerk VARCHAR(15),
    o_shippriority INT,
    o_comment VARCHAR(79)
);

WITH customer AS
(
    SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
    FROM customer_temp
),
    orders AS
(
    SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment
    FROM orders_temp
)

SELECT c.c_name, o.o_orderkey, o.o_orderdate, o.o_totalprice
FROM customer c
INNER JOIN orders o ON c.c_custkey = o.o_custkey
WHERE c.c_nationkey = 1 AND o.o_orderstatus = 'O' AND o.o_orderdate >= '1995-01-01' AND o.o_orderdate < '1996-01-01'
ORDER BY o.o_totalprice DESC;

-- REMORPH CLEANUP: DROP TABLE customer_temp;
-- REMORPH CLEANUP: DROP TABLE orders_temp;