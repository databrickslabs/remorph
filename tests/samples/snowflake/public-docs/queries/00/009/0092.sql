-- see https://docs.snowflake.com/en/sql-reference/sql/alter-materialized-view

ALTER MATERIALIZED VIEW my_mv CLUSTER BY(i);