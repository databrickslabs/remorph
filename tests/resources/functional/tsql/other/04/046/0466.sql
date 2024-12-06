-- tsql sql:
SELECT product_name, order_total FROM ( VALUES ('Product A', 1000), ('Product B', 2000), ('Product C', 3000) ) AS TempResult (product_name, order_total);
