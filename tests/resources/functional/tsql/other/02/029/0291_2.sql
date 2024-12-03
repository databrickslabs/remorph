--Query type: DML
INSERT INTO sales (sales_id, customer_id, order_id)
SELECT *
FROM (
    VALUES (1, 100, 1),
           (2, 200, 2),
           (3, 300, 3)
) AS sales (sales_id, customer_id, order_id);
