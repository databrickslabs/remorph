--Query type: DML
INSERT INTO #orders (order_id, customer_id)
SELECT order_id, customer_id
FROM (
    VALUES (1, 10), (2, 20), (3, 30)
) AS temp_result_set(order_id, customer_id);
