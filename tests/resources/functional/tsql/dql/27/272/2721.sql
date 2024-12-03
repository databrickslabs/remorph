--Query type: DQL
SELECT QUOTENAME('customer name') AS customer_name FROM (VALUES ('customer name')) AS customer (customer_name);
