-- see https://docs.snowflake.com/en/sql-reference/collation

create or replace table test_table (col1 varchar, col2 varchar);
insert into test_table values ('ı', 'i');