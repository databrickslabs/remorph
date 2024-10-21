--Query type: DQL
SELECT m.definition FROM (VALUES(OBJECT_ID('customer_orders'))) AS v(object_id) JOIN sys.sql_modules m ON v.object_id = m.object_id WHERE m.object_id = OBJECT_ID('customer_orders');