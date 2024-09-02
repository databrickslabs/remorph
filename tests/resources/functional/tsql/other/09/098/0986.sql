--Query type: DDL
SELECT *
FROM (
    VALUES
        (1, 100, '2020-01-01', 1, 'Product A'),
        (2, 200, '2020-01-02', 1, 'Product B'),
        (3, 300, '2020-01-03', 2, 'Product C')
) AS orders (
    order_id,
    order_total,
    order_date,
    customer_id,
    product_name
);