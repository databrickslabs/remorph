-- see https://docs.snowflake.com/en/sql-reference/sql/insert-multi-table

INSERT ALL
  INTO t1 VALUES ($1, an_alias, "10 + 20")
SELECT 1, 50 AS an_alias, 10 + 20;