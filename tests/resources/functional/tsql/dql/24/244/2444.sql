--Query type: DQL
SELECT CAST((SELECT 'customer1' AS customer_name, 100 AS customer_id FROM (VALUES ('customer1', 100), ('customer2', 200)) AS customers(customer_name, customer_id) FOR XML PATH('')) AS VARCHAR(MAX)) AS XMLDATA;
