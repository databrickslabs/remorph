--Query type: DML
WITH orders_cte AS (
    SELECT orderkey, custkey, orderstatus
    FROM (
        VALUES (1, 1, 'O'),
               (2, 2, 'O'),
               (3, 3, 'O')
    ) AS orders(orderkey, custkey, orderstatus)
)
SELECT *
FROM orders_cte;

SELECT *
FROM (
    VALUES (1, 1, 'O'),
           (2, 2, 'O'),
           (3, 3, 'O')
) AS orders(orderkey, custkey, orderstatus);