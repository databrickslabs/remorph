-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

CREATE MATERIALIZED VIEW et1_mv
  AS
  SELECT col2 FROM et1;