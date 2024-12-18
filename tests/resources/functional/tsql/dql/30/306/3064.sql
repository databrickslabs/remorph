-- tsql sql:
SELECT length = DATALENGTH(product_name), product_name FROM (VALUES ('Product A'), ('Product B'), ('Product C')) AS products (product_name) ORDER BY product_name;
