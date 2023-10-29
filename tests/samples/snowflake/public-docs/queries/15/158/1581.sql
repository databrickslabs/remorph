-- see https://docs.snowflake.com/en/sql-reference/constructs/order-by

SELECT column1
FROM VALUES (1), (null), (2), (null), (3)
ORDER BY column1;


SELECT column1
FROM VALUES (1), (null), (2), (null), (3)
ORDER BY column1 NULLS FIRST;


SELECT column1
FROM VALUES (1), (null), (2), (null), (3)
ORDER BY column1 DESC;


SELECT column1
FROM VALUES (1), (null), (2), (null), (3)
ORDER BY column1 DESC NULLS LAST;
