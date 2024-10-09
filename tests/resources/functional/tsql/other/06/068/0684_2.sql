--Query type: DML
INSERT INTO new_orders (order_id, product_id, quantity)
SELECT *
FROM (
    VALUES
        (1, 101, 10),
        (2, 102, 20),
        (3, 103, 30)
) AS temp (order_id, product_id, quantity);