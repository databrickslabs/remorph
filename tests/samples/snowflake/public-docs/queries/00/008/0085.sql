-- see https://docs.snowflake.com/en/sql-reference/sql/alter-external-table

ALTER EXTERNAL TABLE et2 ADD PARTITION(col1='2022-01-24', col2='a', col3='12') LOCATION '2022/01';