-- tsql sql:
CREATE TABLE customers
(
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255)
);

CREATE TABLE orders
(
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    CONSTRAINT FK__orders__customer_id__customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

WITH customers_data AS
(
    SELECT 1 AS customer_id, 'John Doe' AS customer_name
),
orders_data AS
(
    SELECT 1 AS order_id, 1 AS customer_id, '2022-01-01' AS order_date
)
INSERT INTO customers (customer_id, customer_name)
SELECT customer_id, customer_name FROM customers_data;

INSERT INTO orders (order_id, customer_id, order_date)
SELECT order_id, customer_id, order_date FROM orders_data;

ALTER TABLE orders NOCHECK CONSTRAINT FK__orders__customer_id__customers;

ALTER TABLE orders CHECK CONSTRAINT FK__orders__customer_id__customers;

SELECT * FROM customers;

SELECT * FROM orders;

-- REMORPH CLEANUP: DROP TABLE customers;

-- REMORPH CLEANUP: DROP TABLE orders;
