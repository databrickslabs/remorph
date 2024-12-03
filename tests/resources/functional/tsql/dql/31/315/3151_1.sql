--Query type: DQL
WITH orders AS (SELECT * FROM (VALUES (1, '2020-01-01', 100.00), (2, '2020-01-02', 200.00)) AS orders (order_id, order_date, total_amount)),
    lineitems AS (SELECT * FROM (VALUES (1, 1, 10.00), (2, 1, 20.00), (3, 2, 30.00)) AS lineitems (lineitem_id, order_id, extended_price))
SELECT o.order_id, l.lineitem_id
FROM orders o
CROSS APPLY (
    SELECT li.lineitem_id, li.extended_price
    FROM lineitems li
    WHERE li.order_id = o.order_id
) AS l
WHERE l.extended_price LIKE N'10.00%';
