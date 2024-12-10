-- tsql sql:
CREATE SEQUENCE seq_orders;
CREATE TABLE orders_demo (
    o_orderkey INTEGER,
    o_custkey INTEGER
);
INSERT INTO orders_demo (
    o_orderkey,
    o_custkey
)
SELECT NEXT VALUE FOR seq_orders, 1;
SELECT * FROM orders_demo;
-- REMORPH CLEANUP: DROP TABLE orders_demo;
-- REMORPH CLEANUP: DROP SEQUENCE seq_orders;
