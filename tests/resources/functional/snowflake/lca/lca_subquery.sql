-- snowflake sql:
SELECT column_a as cid
FROM my_table
WHERE cid in (select cid as customer_id from customer_table where customer_id = '123');
-- databricks sql:
SELECT column_a as cid
FROM my_table
WHERE column_a in (select cid as customer_id from customer_table where cid = '123');
