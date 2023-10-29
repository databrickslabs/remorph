-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

create external table et2(
  col1 date as (parse_json(metadata$external_table_partition):COL1::date),
  col2 varchar as (parse_json(metadata$external_table_partition):COL2::varchar),
  col3 number as (parse_json(metadata$external_table_partition):COL3::number))
  partition by (col1,col2,col3)
  location=@s2/logs/
  partition_type = user_specified
  file_format = (type = parquet);