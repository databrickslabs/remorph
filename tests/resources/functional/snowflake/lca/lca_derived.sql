-- snowflake sql:
SELECT column_a as cid
FROM (select column_x as column_a, column_y as y from my_table where y = '456')
WHERE cid = '123';
-- databricks sql:
SELECT column_a as cid
FROM (select column_x as column_a, column_y as y from my_table where column_y = '456')
WHERE column_a = '123';
