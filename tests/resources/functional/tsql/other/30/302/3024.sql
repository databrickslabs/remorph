--Query type: DCL
SET QUOTED_IDENTIFIER ON;

WITH temp_result AS (
    SELECT id, name, balance, country, address, phone, comment
    FROM (
        VALUES (1, 'John', 100.00, 'USA', '123 Main St', '123-456-7890', 'This is a comment'),
               (2, 'Jane', 200.00, 'Canada', '456 Elm St', '987-654-3210', 'This is another comment')
    ) AS temp_result (id, name, balance, country, address, phone, comment)
),

     temp_orders AS (
    SELECT order_id, customer_id, total
    FROM (
        VALUES (1, 1, 1000.00),
               (2, 1, 2000.00),
               (3, 2, 3000.00)
    ) AS temp_orders (order_id, customer_id, total)
),

     temp_lineitem AS (
    SELECT order_id, price, discount
    FROM (
        VALUES (1, 100.00, 0.10),
               (2, 200.00, 0.20),
               (3, 300.00, 0.30)
    ) AS temp_lineitem (order_id, price, discount)
),

     filtered_lineitem AS (
    SELECT order_id
    FROM temp_lineitem
    GROUP BY order_id
    HAVING SUM(price * (1 - discount)) > 1000.00
)

SELECT tr.id, tr.name, SUM(tli.price * (1 - tli.discount)) AS revenue, tr.balance, tr.country, tr.address, tr.phone, tr.comment
FROM temp_result tr
JOIN temp_orders tos ON tr.id = tos.customer_id
JOIN temp_lineitem tli ON tos.order_id = tli.order_id
JOIN filtered_lineitem fl ON tli.order_id = fl.order_id
WHERE tr.balance > 0.00
GROUP BY tr.id, tr.name, tr.balance, tr.country, tr.address, tr.phone, tr.comment
ORDER BY revenue DESC