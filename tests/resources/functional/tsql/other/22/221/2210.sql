-- tsql sql:
INSERT INTO orders (order_id, customer_id, order_date)
SELECT order_id, customer_id, order_date
FROM (
    VALUES
        (1, 1, '2020-01-01'),
        (2, 2, '2020-01-15'),
        (3, 3, '2020-02-01'),
        (4, 4, '2020-03-01'),
        (5, 5, '2020-04-01')
) AS temp_result (order_id, customer_id, order_date);
