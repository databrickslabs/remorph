--Query type: DDL
CREATE TABLE sales.order_items (order_id INT, product_id INT, quantity INT, CONSTRAINT order_id_un UNIQUE (order_id));
WITH temp AS (
    SELECT *
    FROM (
        VALUES (1, 1, 1), (2, 2, 2)
    ) AS temp (order_id, product_id, quantity)
)
INSERT INTO sales.order_items
SELECT *
FROM temp
