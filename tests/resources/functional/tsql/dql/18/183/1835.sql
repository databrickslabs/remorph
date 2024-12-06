-- tsql sql:
DECLARE @customer_id UNIQUEIDENTIFIER = NEWID();
WITH customer_char AS (
    SELECT CONVERT(CHAR(255), @customer_id) AS customer_char
)
SELECT * FROM customer_char;
