--Query type: DQL
SELECT product_name FROM (VALUES ('chain ring'), ('full face helmet'), ('road bike')) AS products (product_name) WHERE product_name LIKE '%chain%' OR product_name LIKE '%full%';