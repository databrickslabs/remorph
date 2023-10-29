-- see https://docs.snowflake.com/en/sql-reference/sql/alter-table

ALTER TABLE t1 CLUSTER BY (date, id);