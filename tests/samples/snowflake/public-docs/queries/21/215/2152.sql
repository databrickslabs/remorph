-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

select * from example_table sample system (10 rows);

select * from example_table sample row (10 rows) seed (99);