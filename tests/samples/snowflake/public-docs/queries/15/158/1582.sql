-- see https://docs.snowflake.com/en/sql-reference/constructs/order-by

SELECT column1
FROM VALUES (3), (4), (null), (1), (2), (6), (5), (0005), (.05), (.5), (.5000)
ORDER BY column1;
