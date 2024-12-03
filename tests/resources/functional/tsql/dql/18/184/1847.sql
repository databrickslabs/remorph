--Query type: DQL
DECLARE @customer_name NCHAR(12);
SET @customer_name = N'Customer#000000001';
SELECT UNICODE(@customer_name), NCHAR(UNICODE(@customer_name))
FROM (VALUES (1)) AS t(c);
