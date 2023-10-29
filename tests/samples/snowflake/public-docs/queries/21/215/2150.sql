-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

select * from (select * from example_table) sample (1) seed (99);