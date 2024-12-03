--Query type: DQL
DECLARE @customer_id UNIQUEIDENTIFIER = NEWID();
WITH customer AS (
    SELECT CONVERT(CHAR(255), @customer_id) AS customer_char,
           'Customer1' AS customer_name
)
SELECT customer_char,
       customer_name
FROM customer;
