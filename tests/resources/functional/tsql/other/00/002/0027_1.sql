-- tsql sql:
IF OBJECT_ID('customer_order', 'U') IS NOT NULL
    DROP TABLE customer_order;

CREATE TABLE customer_order
(
    order_key INT,
    customer_name VARCHAR(255),
    order_date DATE
);

INSERT INTO customer_order (order_key, customer_name, order_date)
VALUES
    (1, 'John Smith', '2020-01-01'),
    (2, 'Jane Doe', '2020-01-15'),
    (3, 'Bob Johnson', '2020-02-01');

SELECT *
FROM customer_order;
-- REMORPH CLEANUP: DROP TABLE customer_order;
