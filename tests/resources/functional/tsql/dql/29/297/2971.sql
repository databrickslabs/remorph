-- tsql sql:
WITH CustomerCTE AS (
    SELECT customer_id, customer_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS CustomerTable(customer_id, customer_name)
),
OrderCTE AS (
    SELECT order_id, customer_id, order_date
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 1, '2020-01-15')
    ) AS OrderTable(order_id, customer_id, order_date)
),
LineitemCTE AS (
    SELECT order_id, lineitem_id, quantity
    FROM (
        VALUES (1, 1, 10),
               (1, 2, 20),
               (2, 1, 30)
    ) AS LineitemTable(order_id, lineitem_id, quantity)
)
SELECT c.customer_id AS CustomerID,
       c.customer_name AS CustomerName,
       o.order_id AS OrderID,
       o.order_date AS OrderDate,
       l.lineitem_id AS LineitemID,
       l.quantity AS Quantity
FROM CustomerCTE c
     JOIN OrderCTE o ON c.customer_id = o.customer_id
     JOIN LineitemCTE l ON o.order_id = l.order_id
WHERE c.customer_name = 'Customer1'
      AND o.order_date >= '2020-01-01'
      AND l.quantity > 10;
