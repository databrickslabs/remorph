-- see https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view

CREATE MATERIALIZED VIEW mymv
    COMMENT='Test view'
    AS
    SELECT col1, col2 FROM mytable;