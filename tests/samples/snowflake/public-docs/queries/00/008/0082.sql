-- see https://docs.snowflake.com/en/sql-reference/sql/alter-dynamic-table

ALTER DYNAMIC TABLE product SET
  TARGET_LAG = '1 hour';