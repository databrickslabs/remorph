-- tsql sql:
SELECT product_description, order_total FROM (VALUES ('Product A', 100.0), ('Product B', 200.0), ('Product C', 300.0)) AS orders (product_description, order_total) ORDER BY order_total;