--Query type: DDL
CREATE PARTITION FUNCTION pf_orders (int) AS RANGE RIGHT FOR VALUES (100, 500, 1000);
CREATE TABLE orders (
    order_id int,
    order_value int
) ON pf_orders (order_value);
INSERT INTO orders (order_id, order_value)
VALUES (1, 50), (2, 150), (3, 550), (4, 1050);
SELECT * FROM orders;
