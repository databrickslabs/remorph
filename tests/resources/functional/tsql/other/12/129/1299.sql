--Query type: DDL
CREATE TABLE sales.order_items
(
    order_id INT NOT NULL
    CONSTRAINT order_items_constraint UNIQUE,
    product_id INT NOT NULL,
    quantity INT NOT NULL
);
-- REMORPH CLEANUP: DROP TABLE sales.order_items;