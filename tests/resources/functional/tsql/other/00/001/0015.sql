--Query type: DML
CREATE TABLE customer_orders
(
    order_id INT,
    customer_id INT,
    order_date DATE
);

INSERT INTO customer_orders
(
    order_id,
    customer_id,
    order_date
)
SELECT order_id, customer_id, order_date
FROM (
    VALUES
    (
        1,
        101,
        '2020-01-01'
    ),
    (
        2,
        102,
        '2020-01-15'
    ),
    (
        3,
        103,
        '2020-02-01'
    ),
    (
        4,
        104,
        '2020-03-01'
    )
) AS temp_result_set
(
    order_id,
    customer_id,
    order_date
);

SELECT * FROM customer_orders;