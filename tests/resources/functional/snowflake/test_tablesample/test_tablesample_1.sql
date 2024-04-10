
-- snowflake sql:
select * from (select * from example_table) sample (1) seed (99);

-- databricks sql:
SELECT * FROM (SELECT * FROM example_table) TABLESAMPLE (1 PERCENT) REPEATABLE (99);
