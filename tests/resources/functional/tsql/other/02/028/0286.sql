--Query type: DDL
DROP TABLE IF EXISTS orders_total;
CREATE TABLE orders_total
(
    o_orderkey INT,
    o_totalprice DECIMAL(10, 2),
    o_orderstatus VARCHAR(10)
);
SELECT * FROM orders_total;
-- REMORPH CLEANUP: DROP TABLE orders_total;