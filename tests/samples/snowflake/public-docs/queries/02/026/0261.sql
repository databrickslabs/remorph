-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table

CREATE EXTERNAL TABLE exttable1
  LOCATION=@mystage/logs/
  AUTO_REFRESH = true
  FILE_FORMAT = (TYPE = PARQUET)
  ;