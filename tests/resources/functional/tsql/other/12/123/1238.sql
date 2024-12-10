-- tsql sql:
WITH CustomerCTE AS (
    SELECT customer_id, customer_name
    FROM (
        VALUES (1, 'John Doe'),
               (2, 'Jane Doe')
    ) AS Customer(customer_id, customer_name)
),
OrdersCTE AS (
    SELECT order_id, customer_id, order_date
    FROM (
        VALUES (1, 1, '2022-01-01'),
               (2, 1, '2022-01-15'),
               (3, 2, '2022-02-01')
    ) AS Orders(order_id, customer_id, order_date)
)
SELECT c.customer_id, c.customer_name, o.order_id, o.order_date
INTO #CustomerOrders
FROM CustomerCTE c
INNER JOIN OrdersCTE o ON c.customer_id = o.customer_id
OPTION (MAXDOP 1);

SELECT * FROM #CustomerOrders;
-- REMORPH CLEANUP: DROP TABLE #CustomerOrders;
