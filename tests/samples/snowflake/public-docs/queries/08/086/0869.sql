-- see https://docs.snowflake.com/en/sql-reference/literals-table

SELECT * FROM TABLE('mytable');

SELECT * FROM TABLE($$mytable$$);