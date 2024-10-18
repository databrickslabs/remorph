--Query type: DDL
CREATE TABLE orders_table
(
    o_orderkey INT,
    o_custkey INT
);

INSERT INTO orders_table
SELECT o_orderkey, o_custkey
FROM orders;

CREATE CLUSTERED INDEX idx_orders
ON orders_table (o_orderkey)
WITH (ONLINE = ON (WAIT_AT_LOW_PRIORITY (MAX_DURATION = 5 MINUTES, ABORT_AFTER_WAIT = SELF)));

SELECT *
FROM orders_table;

-- REMORPH CLEANUP: DROP TABLE orders_table;