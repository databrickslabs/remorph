-- tsql sql:
WITH temp_result AS (SELECT * FROM (VALUES ('customer1', 100), ('customer2', 200), ('customer3', 300)) AS customers (customer_name, order_total))
SELECT *
FROM temp_result
WHERE order_total IN (
    SELECT TOP 100 order_total
    FROM (VALUES ('order1', 100), ('order2', 200), ('order3', 300)) AS orders (order_name, order_total)
    ORDER BY order_total
);
